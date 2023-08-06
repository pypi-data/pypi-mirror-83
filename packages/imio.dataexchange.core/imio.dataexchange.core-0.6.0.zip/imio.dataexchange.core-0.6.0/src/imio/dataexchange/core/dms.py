# encoding: utf-8

from datetime import datetime


class DMSFile(object):

    def __init__(self, document):
        self._doc = document

    @property
    def file_metadata(self):
        return self._doc.file_metadata

    @property
    def filename(self):
        return self._doc.file_metadata.get('filename')

    @property
    def file_md5(self):
        return self._doc.file_md5

    @property
    def creator(self):
        return self._doc.file_metadata.get('creator')

    @property
    def client_id(self):
        return self._doc.client_id

    @property
    def external_id(self):
        return self._doc.external_id

    @property
    def version(self):
        return self._doc.version

    @property
    def scan_date(self):
        date = '{0} {1}'.format(self._doc.file_metadata.get('scan_date'),
                                self._doc.file_metadata.get('scan_hour'))
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    @property
    def mail_type(self):
        return None


class IncomingMail(DMSFile):
    """A DMS Incoming Mail"""

    @property
    def mail_type(self):
        return 'courrier'


class OutgoingMail(DMSFile):
    """A DMS Outgoing Mail"""


class OutgoingGeneratedMail(DMSFile):
    """A DMS Outgoing Generated Mail"""


class Deliberation(DMSFile):
    """A Deliberation of Plone Meeting"""


class IncomingEmail(DMSFile):
    """ A DMS Incoming Email """
