from enum import Enum


class Databases(str, Enum):
    PostgreSQl = "PostgreSQL"
    MySQL = "MySQL"


class PostgreSQLDrivers(str, Enum):
    ASYNC_DRIVER = "asyncpg"


class MySQLDrivers(str, Enum):
    ASYNC_DRIVER = "asyncmy"
