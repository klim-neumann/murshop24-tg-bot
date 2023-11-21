import enum

PYTZ_TIMEZONE = "Asia/Almaty"


class CallbackData(enum.StrEnum):
    START = enum.auto()
    CATALOG = enum.auto()
    ORDERS = enum.auto()
    RULES = enum.auto()
    FAQ = enum.auto()
    CREATE_ORDER = enum.auto()
