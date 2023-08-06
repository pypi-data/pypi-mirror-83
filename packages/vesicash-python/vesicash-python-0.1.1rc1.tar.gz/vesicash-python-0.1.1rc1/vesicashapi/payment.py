""" Script to call the payment service"""

from vesicashapi.base import VesicashBase

class Payment(VesicashBase):
    
    """
    Collect payment for transaction
    """
    @classmethod
    def pay(cls, **kwargs):
        return cls().requests.post('payment/pay', data=kwargs)
    
    """
    Initiate Manual Disbursement
    """
    @classmethod
    def init_manual_disbursement(cls, **kwargs):
        return cls().requests.post('payment/disbursement/wallet/withdraw', data=kwargs)