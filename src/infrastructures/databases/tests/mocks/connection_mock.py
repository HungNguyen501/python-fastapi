"""Redis Mock"""


# pylint: disable=C0115,C0116,W0613,W0212,W0106,W0107
class DbConnectionMock:
    async def __aenter__(self,):
        """Enter context manager"""
        return self

    async def __aexit__(self, *_):
        """Exit context manager"""
        pass


# pylint: disable=C0115,C0116,W0613,W0212,W0106
class RedisMock:
    """Mock Redis class"""
    async def __aenter__(self,):
        return self

    async def __aexit__(self, *_):
        pass

    async def set(self, name, value, *_):
        pass

    async def get(self, name, *_):
        return "pong"
