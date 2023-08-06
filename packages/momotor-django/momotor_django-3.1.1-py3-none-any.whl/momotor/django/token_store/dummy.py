import typing

from momotor.django.token_store.base import BaseTokenStore


class DummyTokenStore(BaseTokenStore):
    """ Token store that does not save tokens at all
    """
    async def get(self) -> typing.Optional[str]:
        return None

    async def set(self, token: str):
        pass

    async def delete(self):
        pass
