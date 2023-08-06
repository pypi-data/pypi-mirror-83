"""Exceptions (and keywords for raising them) to be used with RPADriver."""


class BusinessException(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class ContinuableApplicationException(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class FatalApplicationException(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = True


class ExceptionRaisers:
    def raise_business_exception(self, msg):
        raise BusinessException(msg)

    def raise_application_exception(self, msg, fatal=True):
        if fatal:
            raise FatalApplicationException(msg)
        else:
            raise ContinuableApplicationException(msg)
