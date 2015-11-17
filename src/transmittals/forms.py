# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Field

from default_documents.layout import DocumentFieldset, DateField

from documents.forms.models import BaseDocumentForm
from transmittals.layout import RelatedRevisionsLayout
from transmittals.models import (
    Transmittal, TransmittalRevision, OutgoingTransmittal,
    OutgoingTransmittalRevision)


class TransmittalForm(BaseDocumentForm):
    def build_layout(self):
        return Layout(
            Field('tobechecked_dir', type='hidden'),
            Field('accepted_dir', type='hidden'),
            Field('rejected_dir', type='hidden'),
            DocumentFieldset(
                _('General information'),
                'document_key',
                DateField('transmittal_date'),
                DateField('ack_of_receipt_date'),
                'contract_number',
                'originator',
                'recipient',
                'sequential_number',
                self.get_related_documents_layout(),
            )
        )

    class Meta:
        model = Transmittal
        exclude = ('document', 'latest_revision', 'status', 'transmittal_key',
                   'document_type', 'contractor',)


class TransmittalRevisionForm(BaseDocumentForm):
    def build_layout(self):
        fields = (
            _('Revision'),
            DateField('revision_date'),
            DateField('received_date'),
            Field('created_on', readonly='readonly'))

        # native / pdf will be autogenerated
        if self.read_only:
            fields += (
                'native_file',
                'pdf_file')

        return Layout(DocumentFieldset(*fields))

    class Meta:
        model = TransmittalRevision
        exclude = ('document', 'revision', 'trs_status', 'updated_on')


class OutgoingTransmittalForm(BaseDocumentForm):
    def get_related_documents_layout(self):
        related_documents = DocumentFieldset(
            _('Related documents'),
            RelatedRevisionsLayout('related_documents'))
        return related_documents

    def build_layout(self):
        return Layout(
            DocumentFieldset(
                _('General information'),
                'document_key',
                'contract_number',
                'originator',
                'recipient',
                'sequential_number',
                self.get_related_documents_layout(),
            )
        )

    class Meta:
        model = OutgoingTransmittal
        exclude = ('document', 'latest_revision', 'related_documents')


class OutgoingTransmittalRevisionForm(BaseDocumentForm):
    def build_layout(self):
        fields = (
            _('Revision'),
            DateField('revision_date'),
            DateField('received_date'),
            Field('created_on', readonly='readonly'))

        # native / pdf will be autogenerated
        if self.read_only:
            fields += ('pdf_file',)

        return Layout(DocumentFieldset(*fields))

    class Meta:
        model = OutgoingTransmittalRevision
        exclude = ('document', 'revision', 'updated_on')
