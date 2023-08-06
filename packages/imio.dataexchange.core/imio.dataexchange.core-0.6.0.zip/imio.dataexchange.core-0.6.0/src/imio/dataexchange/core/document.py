# encoding: utf-8


def create_document(source):
    """Create a Document instance from a source"""
    kw = {}
    for attr in Document.attrs:
        kw[attr] = getattr(source, attr)
    return Document(**kw)


class Document(object):
    """A GED Document"""
    attrs = ('external_id',
             'client_id',
             'type',
             'version',
             'date',
             'update_date',
             'user',
             'file_md5',
             'file_metadata')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def routing_key(self):
        """Return the routing key of the message"""
        return self.client_id
