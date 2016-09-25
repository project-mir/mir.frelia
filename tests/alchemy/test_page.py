import datetime
from unittest import mock

import pytest

import mir.frelia.alchemy as alchemy
from mir.frelia.document import Document
from mir.frelia.page import Page


def render_doc(documents):
    """Simple document renderer."""
    for document in documents:
        yield document._replace(body='rendered ' + document.body)


@pytest.mark.parametrize('text,expected', [
    ('hi', 'rendered hi'),
])
def test_lift_page(text, expected):
    page = Page(mock.sentinel.dummy, Document({}, text))
    page_func = alchemy.LiftPage(render_doc)
    got = page_func([page])
    assert list(got) == [Page(mock.sentinel.dummy, Document({}, expected))]


def test_rebase_page_path():
    page = Page('root/blog/post', mock.sentinel.dummy)
    transform = alchemy.RebasePagePath('root')
    got = transform([page])
    assert list(page.path for page in got) == ['blog/post']


@pytest.mark.parametrize('path,header,expected', [
    ('blog/2010/01/02/post', {}, {'published': datetime.date(2010, 1, 2)}),
    ('blog/2010/01/02/post', {'published': 1}, {'published': 1}),
    ('blog/post', {}, {}),
    ('blog/2010/13/02/post', {}, {}),
    ('blog/2010/01/tag/post', {}, {}),
])
def test_date_from_path(path, header, expected):
    page = Page(path, Document(header, ''))
    transform = alchemy.SetDateFromPath('published')
    got = transform([page])
    assert list(page.document.header for page in got) == [expected]
