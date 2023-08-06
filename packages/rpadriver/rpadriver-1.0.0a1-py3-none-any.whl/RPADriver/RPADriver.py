from copy import deepcopy

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.running.model import TestCase
from TOSLibrary import TOSLibrary
from TOSLibrary.dynamic_library import DynamicLibrary

from RPALibrary.helpers import (
    get_stage_from_tags
)

from .helpers import (
    get_error_handler_from_tags,
    stage_is_transactional,
    test_timed_out
)
from .exceptions import ExceptionRaisers


class RPADriver(DynamicLibrary):  # noqa

    """
    =========
    RPADriver
    =========

    RPADriver is a tool that adds transaction management for RPA automations, where the top-level workflow
    has been defined natively in Robot Framework script. The library has been implemented as a listener,
    see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface.
    In the backend, the RPADriver uses Task Object Storage (TOS), meaning that it relies on MongoDB
    for work item persistance.

    For more information about TOS, see https://intelligent_automation.gitlab-siili.io/tos/
    For more information about Robot Framework, see http://robotframework.org.

    Background
    ----------

    RPA processes usually consist of sequential stages. Some stages are to be executed only once (batch).
    Others are transactional, where identical steps are performed to a number of work items in a
    repetitive manner. RPADriver automates the management of task iterations and work items during
    transactional stages.

    Usage
    -----

    After installation, ``RPADriver`` can be imported in the Settings-table.

    .. code :: robotframework

      *** Settings ***
      Library    RPADriver    ${db_server}:${db_port}    ${db_name}

    Database connection details (address, credentials) are passed to the library using the convention from TOS,
    see https://intelligent_automation.gitlab-siili.io/tos/#usage.

    Task Tags
    ---------
    RPADriver requires special tags to be set on the robot tasks in order to use them as RPA process stages.
    Each task should be assigned a tag prefixed with ``stage_`` depending on its sequence in the process,

    Transactional stages, whose steps are to be repeated for each applicable work item,
    are marked with ``repeat`` tag.

    Example process consisting of one batch stage followed by one transactional stage:

    .. code :: robotframework

        *** Tasks ***
        Initial Stage
            [Tags]    stage_0
            Log    This is performed only once

        Process transactions A
            [Tags]    stage_1    repeat
            Log    Processing item '${ITEM_ID}'

    Working with items
    ------------------

    In transactional stages, RPADriver sets the workable items to the robot scope for each task iteration.
    The work item's payload contents can be accessed in a dictionary named ``${ITEM}``.
    The MongoDB ObjectId of the work item can be accessed as ``{ITEM_ID}`` (str).
    The name of the dictionary variable can be overriden using the ``item_variable_name`` upon library import.
    For example, if you want to refer to the work item as ``&{PERSON}`` in your script:

    .. code :: robotframework
        Library     RPADriver    db_server=localhost    db_name=newtos    item_variable_name=PERSON


    RPADriver exposes ``Update Current Item`` keyword, that can be used in a transactional stage
    to update the payload contents of the currently worked item, e.g. adding a key-value pair.
    The keyword is used similarly to ``Collections.Set To Dictionary``, except that the targeted
    dictionary is omitted, see
    https://robotframework.org/robotframework/latest/libraries/Collections.html#Set%20To%20Dictionary.

    .. code :: robotframework
       | Update Current Item | my_new_key=my_new_value | another_key=another_value |

    or

    .. code :: robotframework
       | Update Current Item | my_new_key | my_new_value | another_key | another_value |

    Setups and Teardowns
    --------------------
    Default test setups and teardowns, (i.e. those set in ``Settings``) are run for each stage.
    Any setups/teardowns set on the robot task with ``[Setup]`` and ``[Teardown]``override their
    default counterparts.

    ``Suite Setup/Teardown`` set in ``Settings`` are run as per normal,
    i.e. only at the beginning and end of the robot execution.

    Task Naming
    --------------

    Task iterations are named according to the worked item. The name determines appears
    in the robot log file. By default, RPADriver uses the MongoDB Object-id as task name,
    but any field from the payload can be used by specifying ``item_identifier_field``
    upon library import. For example, in order to use the values from field ``payload.myField``,
    RPADriver should be imported as follows:

    .. code :: robotframework
        Library     RPADriver    db_server=localhost    db_name=newtos    item_identifier_field=myField

    Error Handling
    --------------

    When processing of a work item fails, robot behaviour depends on the type of error raised.
    RPADriver exposes keywords ``raise_business_exception`` and ``raise_application_exception``.
    The first argument for both keywords is the error message. By default, execution continues
    despite of a failing work item. If an application exception is raised with argument ``fatal``
    set to ``True``, robot execution is stopped, for example:

    .. code :: robotframework
        | Raise Application Exception | Something went terribly wrong | fatal=${TRUE} |

    It is possible to assign a stage-specific error handling keyword, to be run upon failure.
    This is done by tagging the robot task with ``error_handler=[Keyword Name], for example:

    .. code :: robotframework
        *** Tasks ***
        My RPA Stage
            [Tags]    stage_1    repeat    error_handler=Handle My Error
                # ...

    Task timeouts can be used as per normal robot convention. The timeout specified on a stage
    is the maximum time allowed for working one item in said stage. If the timeout is exceeded,
    the item is failed and error handler is called.
    """

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(
        self,
        db_server,
        db_name,
        db_user=None,
        db_passw=None,
        db_auth_source=None,
        item_variable_name="ITEM",
        item_identifier_field=None,
    ):

        super(RPADriver, self).__init__()
        self.ROBOT_LIBRARY_LISTENER = self

        self._item_varname = item_variable_name
        self._item_idfield = item_identifier_field

        self.tos = TOSLibrary(
            db_server=db_server,
            db_name=db_name,
            db_user=db_user,
            db_passw=db_passw,
            db_auth_source=db_auth_source
        )
        self.current_item = None
        self.add_component(self)
        self.add_component(self.tos)
        self.add_component(ExceptionRaisers())

        self.current_stage = None

    @property
    def current_item(self):
        return self.__current_item

    @current_item.setter
    def current_item(self, task_object):
        """Sets two variables to robot scope:
            ${ITEM} is a copy of the work item's payload (dictionary),
            ${ITEM_ID} is the item's MongoDB ObjectId

        By default, ${ITEM} is used as the name of the dictionary variable,
        but this can be overriden upon library import with the ``item_identifier_field`` argument.
        """
        self.__current_item = task_object
        if task_object:
            BuiltIn().set_suite_variable(f"${self._item_varname}", task_object.get("payload"))
            BuiltIn().set_suite_variable(f"$ITEM_ID", task_object["_id"])

    def _start_suite(self, data, result):
        """ Initializes the suite (root-level or process stage)

        For transactional stages (`repeat` in test tags), prepares the initial iteration
        by calling ``_prepare_next_task`` and adds setup and teardown keywords for the stage
        if the stage includes them, or if defaults have been set in the robot Settings-table.

        Non-transactional stages are left untouched.
        """
        task_template = data.tests[0]
        self.current_stage = get_stage_from_tags(task_template.tags)

        if not data.parent:
            # only run once, for the root suite
            self._prepare_root_suite(data)
        elif stage_is_transactional(task_template):
            if task_template.keywords.setup:
                data.keywords.setup = task_template.keywords.setup
            if task_template.keywords.teardown:
                data.keywords.teardown = task_template.keywords.teardown
            self._prepare_next_task(data.tests.pop(0))

    def _prepare_root_suite(self, root_suite):
        """Prepares the suite definition into a runnable RPA process

        This method does not return anything, instead the root suite is manipulated in place.
        In the resulting suite, each robot task is wrapped into its own child suite.
        The stages are automatically sorted based on their numbering (``stage_n`` tags).

        In order for the listener methods to be called, the listener has to be registered in child suites.
        Currently, this is achieved by taking a deepcopy of the root suite to use as the basis of child suites.
        """

        suite_template = deepcopy(root_suite)
        suite_template.tests = []
        suite_template.keywords = []

        for test in sorted(root_suite.tests, key=lambda test: get_stage_from_tags(test.tags)):
            # TODO: Any other way of extending the listener to the child suites?
            suite_wrapper = deepcopy(suite_template)
            suite_wrapper.name = test.name
            suite_wrapper.tests = [test.deepcopy()]
            root_suite.suites.append(suite_wrapper)

        root_suite.tests.clear()

    def _get_item_id(self, item):
        """Returns the value of the item's identifying field.

        By default, ObjectId is used as the id-field but this can be overriden
        upon library import with the ``item_identifier_field`` argument.
        """

        return item["payload"].get(self._item_idfield, None) or str(self.current_item["_id"])

    def _prepare_next_task(self, data: TestCase):
        """ Prepares the task iteration for execution

        Sets a new work item to the robot scope and appends the suite with a copy of the current
        robot task if another workable item for the current stage was found in the database.

        Returns True if a task iteration was added and False otherwise.
        """
        self.current_item = self._get_one_task_object(self.current_stage)
        if self.current_item:
            data.parent.tests.append(RPATask(name=self._get_item_id(self.current_item), task_template=data))
            return True
        else:
            return None

    def _end_test(self, data, result):

        if stage_is_transactional(data) and self.current_item:
            self._update_task_object_stage_and_status(result)

        if not result.passed:
            # TODO: Will future versions of robotframework allow a better way
            #       for inspecting the exception type?
            explicit_error_handler = get_error_handler_from_tags(data.tags)
            if explicit_error_handler:
                BuiltIn().run_keyword_and_ignore_error(explicit_error_handler)

            if "FatalApplicationException" in result.message:
                # Do not prepare another task, robot execution will stop.
                return

            elif "ContinuableApplicationException" in result.message or test_timed_out(result):
                # Proceed to prepare another task.
                pass

        self._prepare_next_task(data)

    # TODO: Is this something that's needed?
    def _rerun_stage_teardown_and_setup(self, current_suite):
        from robot.running import EXECUTION_CONTEXTS as EC
        reset_teardown = current_suite.keywords.teardown.deepcopy()
        reset_teardown.run(EC.current)
        reset_teardown.run(EC.current)

    def _update_task_object_stage_and_status(self, result):

        new_status = "pass" if result.passed else "fail"

        self._update_stage(self.current_item["_id"], self.current_stage)
        self._update_status(self.current_item["_id"], self.current_stage, new_status)

        if not result.passed:
            self._update_exceptions(self.current_item["_id"], self.current_stage, result.message)

    def _get_one_task_object(self, stage=None):
        """
        Gets one work item to be processed by stage with index ``stage``
        """
        if not stage:
            stage = self.current_stage

        getter_args = {
            "statuses": ["pass", "new"],
            "stages": stage - 1,
        }

        return self.tos.find_one_task_object_by_status_and_stage(**getter_args)

    @keyword
    def update_current_item(self, *key_value_pairs, **items):
        """
        Update contents of the currently worked item's payload with the given ``key_value_pairs`` and ``items``.

        Giving items as ``key_value_pairs`` means giving keys and values
        as separate arguments:

        | Set To Dictionary | ${D1} | key | value | second | ${2} |
        =>
        | ${D1} = {'a': 1, 'key': 'value', 'second': 2}

        | Set To Dictionary | ${D1} | key=value | second=${2} |

        The latter syntax is typically more convenient to use, but it has
        a limitation that keys must be strings.

        If given keys already exist in the dictionary, their values are updated.
        """
        dictionary = self.current_item["payload"]

        def set_to_dict():
            if len(key_value_pairs) % 2 != 0:
                raise ValueError(
                    "Adding data to a dictionary failed. There " "should be even number of key-value-pairs."
                )
            for i in range(0, len(key_value_pairs), 2):
                dictionary[key_value_pairs[i]] = key_value_pairs[i + 1]
            dictionary.update(items)
            return dictionary

        self.update_payload(self.current_item["_id"], set_to_dict())
        logger.info(f"Item '{self.current_item['_id']}' contents after update: {self.current_item['payload']}")

    # TODO: Maybe these should be in TOSlibrary
    def _update_stage(self, object_id, current_stage):
        self.tos.set_task_object_stage(object_id, current_stage)
        self.tos.set_stage_start_time(object_id, current_stage)

    def _update_status(self, object_id, current_stage, status):
        self.tos.set_task_object_status(object_id, status)
        self.tos.set_stage_status(object_id, current_stage, status)

    def _update_exceptions(self, object_id, current_stage, value):
        self.tos.set_task_object_last_error(object_id, value)
        self.tos.update_stage_exceptions(object_id, value, current_stage)


class RPATask(TestCase):
    """RPATask object is created for each task iteration in a transactional RPA process stage"""

    def __init__(self, name, task_template):
        super().__init__(
            name=name,
            doc=task_template.doc,
            tags=task_template.tags,
            timeout=task_template.timeout,
            lineno=task_template.lineno,
        )
        self.keywords = task_template.keywords.normal
        self.tags = task_template.tags
