# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import zipfile
import tempfile

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.db import transaction

from documents import signals


@transaction.atomic
def save_document_forms(metadata_form, revision_form, category, **doc_kwargs):
    """Creates or updates a document from it's different forms.

    Two forms are necessary to edit a document : the metadata and revision forms.

    There are multiple cases to handle:

      * We are creating a completely new document
      * We are creating a new revision of an existing document
      * We are editing an existing revision

    """
    if not metadata_form.is_valid():
        raise RuntimeError('Metadata form MUST be valid. \
                           ({})'.format(metadata_form.errors))

    if not revision_form.is_valid():
        raise RuntimeError('Revision form MUST be valid. \
                           ({})'.format(revision_form.errors))

    revision = revision_form.save(commit=False)
    metadata = metadata_form.save(commit=False)

    # Those three functions could be regrouped, but they form
    # an if / else russian mountain
    if metadata.pk is None:
        return create_document_from_forms(metadata_form, revision_form, category, **doc_kwargs)
    elif revision.pk is None:
        return create_revision_from_forms(metadata_form, revision_form, category)
    else:
        return update_revision_from_forms(metadata_form, revision_form, category)


def create_document_from_forms(metadata_form, revision_form, category, **doc_kwargs):
    """Creates a brand new document"""
    from documents.models import Document

    revision = revision_form.save(commit=False)
    revision.revision = revision.get_first_revision_number()
    metadata = metadata_form.save(commit=False)

    key = metadata.document_key or metadata.generate_document_key()
    document = Document.objects.create(
        document_key=key,
        category=category,
        current_revision=revision.revision,
        current_revision_date=revision.revision_date,
        **doc_kwargs)

    revision.document = document
    revision.save()
    revision_form.save_m2m()

    metadata.document = document
    metadata.latest_revision = revision
    metadata.document_key = key
    metadata.save()
    metadata_form.save_m2m()

    signals.document_created.send(
        document=document,
        metadata=metadata,
        revision=revision,
        sender=metadata.__class__)

    return document, metadata, revision


def create_revision_from_forms(metadata_form, revision_form, category):
    """Updates an existing document and creates a new revision."""
    revision = revision_form.save(commit=False)
    metadata = metadata_form.save(commit=False)
    document = metadata.document

    revision.revision = metadata.latest_revision.revision + 1
    revision.document = document
    revision.save()
    revision_form.save_m2m()

    metadata.latest_revision = revision
    metadata.save()
    metadata_form.save_m2m()

    document.current_revision = revision.revision
    document.current_revision_date = revision.revision_date
    document.save()

    signals.document_revised.send(
        document=document,
        metadata=metadata,
        revision=revision,
        sender=metadata.__class__)

    return document, metadata, revision


def update_revision_from_forms(metadata_form, revision_form, category):
    """Updates and existing document and revision."""
    revision = revision_form.save()
    metadata = metadata_form.save()
    document = metadata.document

    signals.revision_edited.send(
        document=document,
        metadata=metadata,
        revision=revision,
        sender=revision.__class__)

    return document, metadata, revision


def compress_documents(documents, format='both', revisions='latest'):
    """Compress the given files' documents (or queryset) in a zip file.

    * format can be either 'both', 'native' or 'pdf'
    * revisions can be either 'latest' or 'all'

    Returns the name of the ziped file.
    """
    temp_file = tempfile.TemporaryFile()

    with zipfile.ZipFile(temp_file, mode='w') as zip_file:
        files = []
        for document in documents:
            if revisions == 'latest':
                revs = [document.latest_revision]
            elif revisions == 'all':
                revs = document.get_all_revisions()

            for rev in revs:
                if rev is not None:
                    if format in ('native', 'both'):
                        files.append(rev.native_file)
                    if format in ('pdf', 'both'):
                        files.append(rev.pdf_file)

        for file_ in files:
            if file_.name:
                zip_file.write(
                    file_.path,
                    file_.name,
                    compress_type=zipfile.ZIP_DEFLATED
                )
    return temp_file


def stringify_value(val, none_val='NC'):
    """Returns a value suitable for display in a document list.

    >>> stringify_value('toto')
    u'toto'

    >>> stringify_value(None)
    u'NC'

    >>> stringify_value(True)
    u'Yes'

    >>> import datetime
    >>> stringify_value(datetime.datetime(2000, 1, 1))
    u'2000-01-01'
    """
    if val is None:
        unicode_val = none_val
    elif type(val) == bool:
        unicode_val = u'Yes' if val else u'No'
    else:
        unicode_val = force_text(val)

    return unicode_val


def get_all_document_types():
    """Return all Metadata content types."""
    from documents.models import Metadata
    qs = ContentType.objects.all()
    types = [ct for ct in qs if issubclass(ct.model_class(), Metadata)]
    return types


def get_all_document_qs():
    """Return all Metadata subclasses as a queryset."""
    types = get_all_document_types()
    ids = [ct.id for ct in types]
    return ContentType.objects.filter(id__in=ids)


def get_all_document_classes():
    """Return all Metadata subclasses available."""
    classes = [ct.model_class() for ct in get_all_document_types()]
    return classes


def get_all_revision_types():
    """Return all MetadataRevision content types."""
    from documents.models import MetadataRevision
    qs = ContentType.objects.all()
    types = (ct for ct in qs if issubclass(ct.model_class(), MetadataRevision))
    return types


def get_all_revision_classes():
    """Return all MetadataRevision subclasses available."""
    classes = [ct.model_class() for ct in get_all_revision_types()]
    return classes
