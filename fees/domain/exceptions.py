class PaidAmountExceedException(ValueError):
    pass


class DuplicateFeeConfigPaidException(ValueError):
    pass


class SameFeeConfigMultipleTimeException(ValueError):
    pass


class NoChangeException(ValueError):
    pass
