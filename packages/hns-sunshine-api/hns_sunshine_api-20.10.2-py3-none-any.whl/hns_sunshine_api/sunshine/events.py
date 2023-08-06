from hns_sunshine_api.sunshine.base import SunshineBase
from requests import Response


class SunshineEvents(SunshineBase):
    """ Sunshine Profiles class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def get_by_profile(self, identifier: str) -> Response:
        """
        Gets Sunshine events linked to a Sunshine profile by profile identifier
        :param identifier: Profile identifier. https://develop.zendesk.com/hc/en-us/articles/360043415094
        :return: Events
        """

        return self._session.get(f'{self._events_base_url}/events', params={'identifier': identifier})

    def get_by_id(self, profile_id: str):
        """
        Gets Sunshine events linked to a Sunshine profile by profile ID
        :param profile_id: Sunshine profile ID
        :return: Events
        """

        return self._session.get(f'{self._events_base_url}/{profile_id}/events')

    def track_against_profile(self, event_data: dict) -> Response:
        """
        Tracks events against a Sunshine profile using Profile Identifier. Identifiers are in event_data
        :param event_data: Event data. https://develop.zendesk.com/hc/en-us/articles/360044045834-Anatomy-of-a-Sunshine-event
        :return: Events
        """

        return self._session.post(f'{self._events_base_url}/events', json=event_data)

    def track_against_profile_id(self, profile_id: str, event_data: dict) -> Response:
        """
        Tracks events against a Sunshine profile using Profile ID
        :param profile_id: Sunshine profile ID
        :param event_data: Event data. https://develop.zendesk.com/hc/en-us/articles/360044045834-Anatomy-of-a-Sunshine-event
        :return: Events
        """

        return self._session.post(f'{self._events_base_url}/{profile_id}/events', json=event_data)

