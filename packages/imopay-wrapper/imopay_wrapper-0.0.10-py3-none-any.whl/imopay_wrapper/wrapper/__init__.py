from .address import AddressWrapper
from .bank_account import BankAccountWrapper
from .company import CompanyWrapper
from .person import PersonWrapper
from .transaction import TransactionWrapper
from .webhook import WebhookWrapper


class ImopayWrapper:
    def __init__(self, *args, **kwargs):
        self.address = AddressWrapper(*args, **kwargs)
        self.bank_account = BankAccountWrapper(*args, **kwargs)
        self.company = CompanyWrapper(*args, **kwargs)
        self.person = PersonWrapper(*args, **kwargs)
        self.transaction = TransactionWrapper(*args, **kwargs)
        self.webhook = WebhookWrapper(*args, **kwargs)
