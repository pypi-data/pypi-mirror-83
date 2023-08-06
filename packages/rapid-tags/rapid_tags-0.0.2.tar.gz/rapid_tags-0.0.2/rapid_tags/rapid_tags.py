# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union
from urllib.parse import quote
import random

# Pip
from kcu import request

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: RapidTags ------------------------------------------------------------ #

class RapidTags:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None
    ):
        self.proxy = proxy
        self.user_agent = user_agent


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def get_tags(
        self,
        title: str,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None,
        debug: bool = False
    ) -> Optional[List[str]]:
        return RapidTags.get_tags_cls(title, proxy or self.proxy, user_agent or self.user_agent, debug=debug)

    @classmethod
    def get_tags_cls(
        cls,
        title: str,
        proxy: Optional[Union[List[str], str]] = None,
        user_agent: Optional[str] = None,
        debug: bool = False
    ) -> Optional[List[str]]:
        try:
            if type(proxy) == list:
                proxy = random.choice(proxy) if len(proxy) > 0 else None

            return [t.replace('\\', '') for t in request.get(
                'https://rapidtags.io/api/generator?query=' + quote(title),
                max_request_try_count=1,
                user_agent=user_agent,
                proxy_ftp=proxy,
                proxy_http=proxy,
                proxy_https=proxy,
                debug=debug
            ).json()['tags']]
        except Exception as e:
            if debug:
                print(e)

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #