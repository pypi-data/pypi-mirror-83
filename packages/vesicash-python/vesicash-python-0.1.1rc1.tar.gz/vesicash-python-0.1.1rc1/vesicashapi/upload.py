""" Script used to call the upload service"""

from vesicashapi.base import VesicashBase

class Upload(VesicashBase):
    @classmethod
    def upload(cls, **kwargs):
        return cls().requests.post('upload/file', data=kwargs)
