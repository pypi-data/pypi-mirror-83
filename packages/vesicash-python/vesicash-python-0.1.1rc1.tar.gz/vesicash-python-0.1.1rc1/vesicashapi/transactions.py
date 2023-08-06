""" Script used to call the transactions service"""

from vesicashapi.base import VesicashBase

class Transactions(VesicashBase):
    @classmethod
    def create(cls, **kwargs):
        return cls().requests.post('transactions/create', data=kwargs)

    @classmethod
    def accept_transaction(cls, **kwargs):
        return cls().requests.post('transactions/accept', data=kwargs)

    @classmethod
    def reject_transaction(cls, **kwargs):
        return cls().requests.post('transactions/reject', data=kwargs)

    @classmethod
    def fetch_transaction(cls, **kwargs):
        transaction_id = kwargs['transaction_id']
        return cls().requests.post('transactions/listById/' + transaction_id, data=Null)

    @classmethod
    def request_due_date_extension(cls, **kwargs):
        return cls().requests.post('transactions/request/due_date_extension', data=kwargs)

    @classmethod
    def approve_due_date_extension(cls, **kwargs):
        return cls().requests.post('transactions/approve/due_date_extension', data=kwargs)

    @classmethod
    def mark_as_delivered(cls, **kwargs):
        return cls().requests.post('transactions/delivered', data=kwargs)

    @classmethod
    def accept_delivered_transaction(cls, **kwargs):
        return cls().requests.post('transactions/satisfied', data=kwargs)

    @classmethod
    def reject_delivered_transaction(cls, **kwargs):
        return cls().requests.post('transactions/reject_delivery', data=kwargs)

    @classmethod
    def list_business_transactions(cls, **kwargs):
        return cls().requests.post('transactions/listByBusiness', data=kwargs)

    @classmethod
    def list_user_transactions(cls, **kwargs):
        return cls().requests.post('transactions/listByUser', data=kwargs)

    @classmethod
    def send_transaction(cls, **kwargs):
        return cls().requests.post('transactions/send', data=kwargs)

    @classmethod
    def add_transaction_parties(cls, **kwargs):
        return cls().requests.post('transactions/parties/update', data=kwargs)

    