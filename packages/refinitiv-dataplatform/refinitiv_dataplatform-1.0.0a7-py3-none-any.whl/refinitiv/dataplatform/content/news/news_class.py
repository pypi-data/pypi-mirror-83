# coding: utf8

__all__ = ["News"]

from .news_headlines import NewsHeadlines
from .news_story import NewsStory
from .sort_order import SortOrder


class News(object):

    @property
    def _headlines(self):
        if self.__headlines is None:
            self.__headlines = NewsHeadlines(self._session, self._on_response)
        return self.__headlines

    @property
    def _story(self):
        if self.__story is None:
            self.__story = NewsStory(self._session, self._on_response)
        return self.__story

    def __init__(self, session, on_response=None):
        if session is None:
            raise AttributeError("Session must be defined")

        session._env.raise_if_not_available('news')

        self._session = session
        self._on_response = on_response

        self.__headlines = None
        self.__story = None

    def get_headlines(
            self,
            query="Topic:TOPALL and Language:LEN",
            count=10,
            date_from=None,
            date_to=None,
            sort_order=SortOrder.new_to_old,
            on_page_response=None,
            closure=None
    ):
        response = self._headlines.get_headlines(
            query,
            count,
            date_from,
            date_to,
            sort_order,
            on_page_response,
            closure
        )
        return response

    async def get_headlines_async(
            self,
            query="Topic:TOPALL and Language:LEN",
            count=10,
            date_from=None,
            date_to=None,
            sort_order=SortOrder.new_to_old,
            on_page_response=None,
            closure=None
    ):
        response = await self._headlines.get_headlines_async(
            query,
            count,
            date_from,
            date_to,
            sort_order,
            on_page_response,
            closure
        )
        return response

    def get_story(
            self,
            story_id,
            closure=None
    ):
        response = self._story.get_story(story_id, closure)
        return response

    async def get_story_async(
            self,
            story_id,
            closure=None
    ):
        response = await self._story.get_story_async(story_id, closure)
        return response
