from dataclasses import dataclass

from .base import BaseImopayObj
from ..validators import validate_obj_attr_in_collection


@dataclass
class BankAccount(BaseImopayObj):
    owner: str
    bank: str
    number: str
    routing: str
    type: str

    VALID_TYPES = {"poupança", "corrente"}

    def _validate_type(self):
        validate_obj_attr_in_collection(self, "type", self.VALID_TYPES)
