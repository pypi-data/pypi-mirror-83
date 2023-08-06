from hns_sunshine_api.sunshine.base import SunshineBase
from requests import Response


class SunshineObjectRecords(SunshineBase):
    """ Sunshine Objects class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def list(self, object_type: str, external_id: str = None, timeout: int = None) -> Response:
        """
        Gets object records from sunshine
        :param object_type: Type of object record
        :param external_id: external ID for the object record
        :param timeout: Request timeout in seconds
        :return: Object record
        """

        params = {
            'type': object_type
        }
        if external_id:
            params['external_id'] = external_id

        return self._session.get(
            f'{self._objects_base_url}/records',
            params=params,
            timeout=timeout
        )

    def list_related(self, object_id: str, relationship_key: str, timeout: int = None) -> Response:
        """
        Returns all the object records that the specified object record has relationship records with for the
        specified relationship type
        :param object_id: Object record ID
        :param relationship_key: Relationship type key
        :param timeout: Request timeout in seconds
        :return: All the object records related to the relationship key
        """

        return self._session.get(
            f'{self._objects_base_url}/records/{object_id}/related/{relationship_key}',
            timeout=timeout
        )

    def show(self, object_id: str, timeout: int = None) -> Response:
        """
        Returns the specified object record
        :param object_id: Object record ID
        :param timeout: Request timeout in seconds
        :return: Object record
        """

        return self._session.get(
            f'{self._objects_base_url}/records/{object_id}',
            timeout=timeout
        )

    def create(self, record_data: dict, timeout: int = None) -> Response:
        """
        Creates an object record.
        :param record_data: Object record data.
        Check https://developer.zendesk.com/rest_api/docs/sunshine/resources#json-format for details
        :param timeout: Request timeout in seconds
        :return: Object record
        """

        return self._session.post(
            f'{self._objects_base_url}/records',
            json=record_data,
            timeout=timeout
        )

    def update(self, object_id: str, data: dict, timeout: int = None) -> Response:
        """
        Updates the attributes object of the specified object record. It does not update any other record properties.

        The attributes object patches the previously stored object. Therefore, the request should only contain the
        properties of the attributes object that need to be updated.

        The request must include an "application/merge-patch+json" content-type header.

        :param object_id: Object record ID
        :param data: Object record
        :param timeout: Request timeout in seconds
        :return: Updated object record
        """

        self._session.headers['Content-type'] = 'application/merge-patch+json'
        return self._session.patch(
            f'{self._objects_base_url}/records/{object_id}',
            json=data,
            timeout=timeout
        )

    def update_by_external_id(self, data: dict, timeout: int = None) -> Response:
        """
        Creates a new object if an object with given external id does not exist and updates the attributes object of
        the specified object record if an object with the given external id does exist.
        This endpoint does not update any other record properties.

        The request data should contain:
            - Object type
            - External id
            - attributes of the object that needs to be updated
        The request must include an "application/merge-patch+json" content-type header.

        :param data: Object record
        :param timeout: Request timeout in seconds
        :return: Updated object record
        """

        self._session.headers['Content-type'] = 'application/merge-patch+json'
        return self._session.patch(
            f'{self._objects_base_url}/records',
            json=data,
            timeout=timeout
        )

    def delete(self, object_id: str, timeout: int = None) -> Response:
        """
        Deletes the specified object record.

        Before deleting an object record, you must delete any relationship record that specifies the object record

        :param object_id: Object record ID
        :param timeout: Request timeout in seconds
        :return: Nothing
        """

        return self._session.delete(
            f'{self._objects_base_url}/records/{object_id}',
            timeout=timeout
        )
