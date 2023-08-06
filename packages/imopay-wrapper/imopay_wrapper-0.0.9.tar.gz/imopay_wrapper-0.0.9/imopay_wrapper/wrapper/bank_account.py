from .base import BaseImopayWrapper, CreateMixin, RetrieveMixin, DestroyMixin
from ..models.bank_account import BankAccount


class BankAccountWrapper(BaseImopayWrapper, CreateMixin, RetrieveMixin, DestroyMixin):
    """
    Wrapper para os métodos de contas bancárias
    """

    @property
    def action(self):
        return "bank_accounts"

    @property
    def model(self):
        return BankAccount
