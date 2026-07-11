from typing import Any
from pydantic import BaseModel


class OAuthToken(BaseModel):
    oauth_token: str
    oauth_token_secret: str


class WikidataOAuth:
    def __init__(
        self,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self._oauth_token: str | None = None
        self._oauth_token_secret: str | None = None

    def get_authorization_url(self, callback_url: str) -> str:
        return f"https://www.wikidata.org/wiki/Special:OAuth/initiate?callback={callback_url}"

    def obtain_request_token(self) -> OAuthToken:
        return OAuthToken(oauth_token="", oauth_token_secret="")

    def exchange_request_token(self, oauth_token: str, oauth_verifier: str) -> None:
        self._oauth_token = oauth_token
        self._oauth_token_secret = oauth_verifier

    @property
    def is_authenticated(self) -> bool:
        return self._oauth_token is not None
