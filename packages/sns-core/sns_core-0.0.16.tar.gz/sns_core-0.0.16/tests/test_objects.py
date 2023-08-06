from unittest import TestCase

from sns_core.exceptions import SNSobjectException
from sns_core.objects import SNSinteraction, SNScontent

class TestSNSObjects(TestCase):

    def test_interaction(self):
        interaction = SNSinteraction("USER", "retrieve", headers={'From':'me','To':'you'}, content={'Content':'Hi'})

        self.assertEqual(interaction.type, "USER")
        self.assertEqual(interaction.action, "retrieve")
        self.assertEqual(interaction.headers, {'From':'me',"To":'you'})
        self.assertEqual(type(interaction.content), SNScontent)
        self.assertEqual(interaction.get('From'), 'me')
        self.assertEqual(interaction.get('To'), 'you')
        self.assertEqual(interaction.get('Missing'), None)
        self.assertEqual(interaction.get('Missing', 'Restore'), 'Restore')
        self.assertMultiLineEqual(str(interaction), "USER retrieve\r\nFrom: me\r\nTo: you\r\n\r\nContent: Hi")

    def test_interaction_without_headers(self):
        interaction = SNSinteraction("USER", "retrieve", content=None)

        self.assertEqual(interaction.type, "USER")
        self.assertEqual(interaction.action, "retrieve")
        self.assertEqual(interaction.headers, {})
        self.assertEqual(type(interaction.content), SNScontent)
        self.assertEqual(interaction.get('From'), None)
        self.assertEqual(interaction.get('To'), None)
        self.assertEqual(interaction.get('Missing'), None)
        self.assertEqual(interaction.get('Missing', 'Restore'), 'Restore')
        self.assertMultiLineEqual(str(interaction), "USER retrieve")

    def test_interaction_without_content(self):
        interaction = SNSinteraction("USER", "retrieve", headers={'From':'me','To':'you'})

        self.assertEqual(interaction.type, "USER")
        self.assertEqual(interaction.action, "retrieve")
        self.assertEqual(interaction.headers, {'From':'me',"To":'you'})
        self.assertEqual(type(interaction.content), SNScontent)
        self.assertEqual(interaction.get('From'), 'me')
        self.assertEqual(interaction.get('To'), 'you')
        self.assertEqual(interaction.get('Missing'), None)
        self.assertEqual(interaction.get('Missing', 'Restore'), 'Restore')
        self.assertMultiLineEqual(str(interaction), "USER retrieve\r\nFrom: me\r\nTo: you")

    def test_content_none(self):
        content = SNScontent()

        self.assertEqual(content.content, {})
        self.assertEqual(content.length(), 0)
        self.assertEqual(len(content), 0)
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), '')

    def test_content_list(self):
        with self.assertRaises(SNSobjectException):
            SNScontent([{'Content':'Test'}, {'Content':'Test2'}])

    def test_content_list_all(self):
        with self.assertRaises(SNSobjectException):
            SNScontent([{'Content':['Test','Test2']}, {'Content':'Test3'}, 'Test: yes', ['Test: yes2']])

    def test_content_str(self):
        content = SNScontent('Content: Test')

        self.assertEqual(content.content, {'Content': 'Test'})
        self.assertEqual(content.length(), 1)
        self.assertEqual(len(content), 1)
        self.assertEqual(content.get('Content'), 'Test')
        self.assertEqual(content.get('Content', 'Restore'), 'Test')
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), 'Content: Test')

    def test_content_str_invalid(self):
        with self.assertRaises(SNSobjectException):
            SNScontent('Content:Test')

    def test_content_bytes(self):
        content = SNScontent(b'Content: Test')

        self.assertEqual(content.content, {'Content': 'Test'})
        self.assertEqual(content.length(), 1)
        self.assertEqual(len(content), 1)
        self.assertEqual(content.get('Content'), 'Test')
        self.assertEqual(content.get('Content', 'Restore'), 'Test')
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), 'Content: Test')

    def test_content_bytes_invalid(self):
        with self.assertRaises(SNSobjectException):
            SNScontent(b'0xd1')

    def test_content_dict(self):
        content = SNScontent({'Content': 'Test'})

        self.assertEqual(content.content, {'Content': 'Test'})
        self.assertEqual(content.length(), 1)
        self.assertEqual(len(content), 1)
        self.assertEqual(content.get('Content'), 'Test')
        self.assertEqual(content.get('Content', 'Restore'), 'Test')
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), 'Content: Test')

    def test_content_dict_list(self):
        content = SNScontent({'Content': 'Test'})

        self.assertEqual(content.content, {'Content': 'Test'})
        self.assertEqual(content.length(), 1)
        self.assertEqual(len(content), 1)
        self.assertEqual(content.get('Content'), 'Test')
        self.assertEqual(content.get('Content', 'Restore'), 'Test')
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), 'Content: Test')

    def test_content_SNScontent(self):
        content = SNScontent(SNScontent({'Content': 'Test'}))

        self.assertEqual(content.content, {'Content': 'Test'})
        self.assertEqual(content.length(), 1)
        self.assertEqual(len(content), 1)
        self.assertEqual(content.get('Content'), 'Test')
        self.assertEqual(content.get('Content', 'Restore'), 'Test')
        self.assertEqual(content.get('Missing'), None)
        self.assertEqual(content.get('Missing', 'Restore'), 'Restore')
        self.assertEqual(str(content), 'Content: Test')