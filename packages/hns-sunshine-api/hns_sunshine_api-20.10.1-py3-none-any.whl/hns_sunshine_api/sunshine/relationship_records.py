from hns_sunshine_api.sunshine.base import SunshineBase
from requests import Response


class SunshineRelationshipRecords(SunshineBase):
    """ Sunshine relationships class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def list_by_object_record(self, object_id: str, relationship_type: str, timeout: int = None) -> Response:
        """
        Returns the relationship records of a specified relationship type for a specified object record.
        For the type, specify a relationship type key. For the object record id, specify a custom object
        record id or a Zendesk object record id.
        The record id must be the relationship record's source record id, not its target record id.

        :param object_id: Object record ID
        :param relationship_type: Relationship type key
        :param timeout: Request timeout
        :return: Relationship record
        """

        return self._session.get(
            f'{self._objects_base_url}/records/{object_id}/relationships/{relationship_type}',
            timeout=timeout
        )

    def list_by_type(self, relationship_type: str, timeout: int = None) -> Response:
        """
        Returns all the relationship records of the specified relationship type.
        For the type, specify a relationship type key.
        :param relationship_type: Relationship type key
        :param timeout: Request timeout
        :return: Relationship records
        """

        return self._session.get(
            f'{self._relationships_base_url}/records',
            params={'type': relationship_type},
            timeout=timeout
        )

    def show(self, relationship_id: str, timeout: int = None) -> Response:
        """
        Returns a relationship record specified by id
        :param relationship_id: Relationship type key
        :param timeout: Request timeout
        :return: Relationship record
        """

        return self._session.get(
            f'{self._relationships_base_url}/records/{relationship_id}',
            timeout=timeout
        )

    def create(self, record_data: dict, timeout: int = None) -> Response:
        """
        Creates a relationship record between two object records based on a relationship type.
        The relationship type defines the object types of the two object records.
        :param record_data: Relationship record data.
        Check https://developer.zendesk.com/rest_api/docs/sunshine/relationships#json-format for details
        :param timeout: Request timeout
        :return: Relationship record
        """

        return self._session.post(
            f'{self._relationships_base_url}/records',
            json=record_data,
            timeout=timeout
        )

    def delete(self, relationship_id: str, timeout: int = None) -> Response:
        """
        Deletes a specified relationship record
        :param relationship_id: Relationship object ID
        :param timeout: Request timeout
        :return: Nothing
        """

        return self._session.delete(
            f'{self._relationships_base_url}/records/{relationship_id}',
            timeout=timeout
        )

