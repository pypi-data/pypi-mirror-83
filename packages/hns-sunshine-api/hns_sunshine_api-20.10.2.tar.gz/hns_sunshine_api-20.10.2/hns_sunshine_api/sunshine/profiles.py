from hns_sunshine_api.sunshine.base import SunshineBase
from requests import Response
from typing import Union, Dict


class SunshineProfiles(SunshineBase):
    """ Sunshine Profiles class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def get_by_identifier(self, identifier: str) -> Response:
        """
        Gets Sunshine profile by identifier
        :param identifier: Profile identifier. https://develop.zendesk.com/hc/en-us/articles/360043415094
        :return: Profile
        """

        return self._session.get(self._profiles_base_url, params={'identifier': identifier})

    def get_by_id(self, profile_id: str) -> Response:
        """
        Gets Sunshine profile by profile ID
        :param profile_id: Sunshine profile ID
        :return: Profile
        """

        return self._session.get(f'{self._profiles_base_url}/{profile_id}')

    def get_by_user_id(self, user_id: str) -> Response:
        """
        Gets Sunshine profile by Zendesk user ID
        :param user_id: Zendesk user ID
        :return: Profiles
        """

        return self._session.get(f'{self._users_base_url}/{user_id}/profiles')

    def profile_exists(self, identifier: str) -> Union[Dict[str, str], None]:
        """
        Checks is a Sunshine profile exists for a given identifier.
        :param identifier: Profile identifier. https://develop.zendesk.com/hc/en-us/articles/360043415094
        :return: If profile exists then returns a dict with keys: user_id (zendesk user id) and profile_id
        else returns None
        """

        profile = self.get_by_identifier(identifier)
        if profile.ok:
            profile_data = profile.json()
            return {'profile_id': profile_data['profile']['id'], 'user_id': profile_data['profile']['user_id']}
        return None

    def create_or_update(self, identifier: str, profile_data: dict) -> Response:
        """
        Creates or updates a profile
        :param identifier: Profile identifier. https://develop.zendesk.com/hc/en-us/articles/360043415094
        :param profile_data: Profile data. https://develop.zendesk.com/hc/en-us/articles/360044532633
        :return: Profile
        """

        return self._session.put(
            self._profiles_base_url,
            params={'identifier': identifier},
            json=profile_data
        )

    def partial_update(self, identifier: str, profile_data: dict) -> Response:
        """
        Partially updates a profile. If the profile does not exists, 404 error is returned.
        https://develop.zendesk.com/hc/en-us/articles/360044129314#patch
        :param identifier: Profile identifier. https://develop.zendesk.com/hc/en-us/articles/360043415094
        :param profile_data: Profile data. https://develop.zendesk.com/hc/en-us/articles/360044532633
        :return: Profile
        """

        return self._session.patch(
            self._profiles_base_url,
            params={'identifier': identifier},
            json=profile_data
        )

    def update_by_id(self, profile_id: str, profile_data: dict) -> Response:
        """
        Updates a profile by profile ID
        :param profile_id: Sunshine profile ID
        :param profile_data: Profile data. https://develop.zendesk.com/hc/en-us/articles/360044532633
        :return: Profile
        """

        return self._session.put(
            f'{self._profiles_base_url}/{profile_id}',
            json=profile_data
        )

    def partial_update_by_id(self, profile_id: str, profile_data: dict) -> Response:
        """
        Partially updates a profile by profile ID. If the profile does not exists, 404 error is returned.
        https://develop.zendesk.com/hc/en-us/articles/360044129314#patch
        :param profile_id: Sunshine profile ID
        :param profile_data: Profile data. https://develop.zendesk.com/hc/en-us/articles/360044532633
        :return: Profile
        """

        return self._session.patch(
            f'{self._profiles_base_url}/{profile_id}',
            json=profile_data
        )

    def delete_profile(self, profile_id: str) -> Response:
        """
        Deletes a Sunshine profile by profile ID
        :param profile_id: Sunshine profile ID
        :return: Just the HTTP status code
        """

        return self._session.delete(f'{self._profiles_base_url}/{profile_id}')
