from enum import Enum


class Servers(Enum):
    """
    UniCatDB API servers
    """
    UNICATDB_ORG = "https://api.unicatdb.org"
    TEST_UNICATDB_ORG = "https://api.test.unicatdb.org"