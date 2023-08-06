from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *

IMG = "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"

class AttachmentTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('test')
        self.client.force_login(user)

    def test(self):
        res = self.client.post('/api/attachments/', {'source':IMG})
        self.assertEqual(res.status_code, 201)


    def test_update(self):
        " 编辑权限测试 "
        res = self.client.put('/api/attachments/0/')
        self.assertEqual(res.status_code, 403)

    def test_delete(self):
        " 删除权限测试 "
        res = self.client.delete('/api/attachments/0/')
        self.assertEqual(res.status_code, 403)
