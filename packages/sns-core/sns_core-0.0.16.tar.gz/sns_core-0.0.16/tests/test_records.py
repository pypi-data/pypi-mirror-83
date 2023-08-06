from unittest import TestCase

from sns_core.records import SNSuserRecordInstance, register_sns_records, check_record_integrity

class TestSNSRecords(TestCase):

    def test_SNSuserRecordInstance(self):
        instance = SNSuserRecordInstance('me', 'sns.provider')

        assert instance.identifier == 'me'
        assert instance.provider == 'sns.provider'