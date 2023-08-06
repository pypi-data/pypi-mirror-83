from .base import (
    BaseImopayWrapper,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    GetByDocumentMixin,
)
from ..models.address import Address


class AddressWrapper(
    BaseImopayWrapper, CreateMixin, UpdateMixin, RetrieveMixin, GetByDocumentMixin
):
    """
    Wrapper para os métodos de address
    """

    @property
    def model(self):
        return Address

    @property
    def action(self):
        return "addresses"

    def create(self, data: dict):
        instance = self.model(**data)
        url = self._construct_url(action=self.action, subaction="create_by_name_and_uf")
        return self._post(url, instance.to_dict())

    def update(self, identifier, data: dict):
        instance = self.model(**data)
        url = self._construct_url(
            action=self.action, subaction="update_by_name_and_uf", identifier=identifier
        )
        return self._patch(url, instance.to_dict())
