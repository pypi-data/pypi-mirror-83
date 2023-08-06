from unittest import TestCase

from sns_core.exceptions import SNSparserException, SNSinteractionException, SNSrecordIntegrityException, SNSobjectException, SNSserverException

class TestSNSexceptions(TestCase):

    def test_message_SNSparserException(self):
        exception = SNSparserException('Test', 'SNSparserException')

        assert exception.interaction == 'Test'
        assert exception.message == 'SNSparserException'
        assert str(exception) == 'Test: SNSparserException'

    def test_SNSparserException(self):
        exception = SNSparserException('Test')

        assert exception.interaction == 'Test'
        assert exception.message == 'Exception occurred while parsing the following interaction'
        assert str(exception) == 'Test: Exception occurred while parsing the following interaction'

    def test_message_SNSinteractionException(self):
        exception = SNSinteractionException('Test', 'SNSinteractionException')

        assert exception.interaction == 'Test'
        assert exception.message == 'SNSinteractionException'
        assert str(exception) == 'Test: SNSinteractionException'

    def test_SNSinteractionException(self):
        exception = SNSinteractionException('Test')

        assert exception.interaction == 'Test'
        assert exception.message == 'Exception occurred while requesting with the following interaction'
        assert str(exception) == 'Test: Exception occurred while requesting with the following interaction'

    def test_message_SNSrecordIntegrityException(self):
        exception = SNSrecordIntegrityException('Test', 'SNSrecordIntegrityException')

        assert exception.record == 'Test'
        assert exception.message == 'SNSrecordIntegrityException'
        assert str(exception) == 'Test: SNSrecordIntegrityException'

    def test_SNSrecordIntegrityException(self):
        exception = SNSrecordIntegrityException('Test')

        assert exception.record == 'Test'
        assert exception.message == 'Exception occurred while checked the integrity of the following record'
        assert str(exception) == 'Test: Exception occurred while checked the integrity of the following record'

    def test_message_SNSobjectException(self):
        exception = SNSobjectException('Test', 'SNSobjectException')

        assert exception.object == 'Test'
        assert exception.message == 'SNSobjectException'
        assert str(exception) == 'Test: SNSobjectException'

    def test_SNSobjectException(self):
        exception = SNSobjectException('Test')

        assert exception.object == 'Test'
        assert exception.message == 'Exception occurred while performing an operation on an SNS object'
        assert str(exception) == 'Test: Exception occurred while performing an operation on an SNS object'

    def test_message_SNSserverException(self):
        exception = SNSserverException('SNSserverException')

        assert exception.message == 'SNSserverException'
        assert str(exception) == 'SNSserverException'

    def test_SNSserverException(self):
        exception = SNSserverException()

        assert exception.message == 'Exception occurred while an operation was performed on the server'
        assert str(exception) == 'Exception occurred while an operation was performed on the server'