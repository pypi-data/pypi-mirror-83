import logging
import liblynx

from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    AuthCredentials,
)
from starlette.datastructures import URL


class WAYFException(AuthenticationError):
    def __init__(self, redirect_to: str = None) -> None:
        self.redirect_to = redirect_to


class LibLynxAuthBackend(AuthenticationBackend):
    def __init__(self):
        self.connect = liblynx.Connect()

    async def authenticate(self, request):
        identification = self.connect.new_identification(
            request.client.host,
            str(URL(scope=request.scope)),
            request.headers.get("User-Agent", "<unknown>"),
        )
        logging.debug("identification in LibLynxAuthBackend is %s",
                      identification["id"])

        if identification["status"] == "identified":
            return (
                AuthCredentials(["authenticated"]),
                SimpleUser(identification["account"]["account_name"]),
            )
        elif identification["status"] == "wayf":
            logging.debug("WAYF needed, asking for %s",
                          identification["_links"]["wayf"]["href"])
            raise WAYFException(identification["_links"]["wayf"]["href"])
