# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.test import TestCase
from django.core import mail
from django.core.management import call_command

from categories.factories import CategoryFactory
from documents.factories import DocumentFactory
from accounts.factories import UserFactory
from reviews.models import Review


class PendingReviewsReminderTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.user = UserFactory(
            email='testadmin@phase.fr',
            password='pass',
            is_superuser=True,
            category=self.category
        )
        self.client.login(email=self.user.email, password='pass')
        self.doc1 = DocumentFactory(
            category=self.category,
            revision={
                'leader': self.user,
                'received_date': datetime.date.today(),
            }
        )
        self.doc2 = DocumentFactory(
            category=self.category,
            revision={
                'leader': self.user,
                'received_date': datetime.date.today(),
            }
        )

    def test_empty_reminder_list(self):
        call_command('send_review_reminders')
        self.assertEqual(len(mail.outbox), 0)

    def test_send_reminders(self):
        self.doc1.get_latest_revision().start_review()
        self.assertEqual(Review.objects.all().count(), 1)

        call_command('send_review_reminders')
        self.assertEqual(len(mail.outbox), 1)

    def test_finished_reviews(self):
        rev = self.doc1.get_latest_revision()
        rev.start_review()
        rev.end_review()
        self.assertEqual(Review.objects.all().count(), 1)

        call_command('send_review_reminders')
        self.assertEqual(len(mail.outbox), 0)