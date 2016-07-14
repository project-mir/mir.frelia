from unittest import mock

import jinja2
import pytest

import frelia.page
import frelia.transforms


def test_transform_group():
    mock_func = mock.Mock()
    transform = frelia.transforms.TransformGroup([mock_func])
    transform([mock.sentinel.object])
    assert mock_func.mock_calls == [mock.call([mock.sentinel.object])]


def test_render_jinja(env, template, document):
    render = frelia.transforms.RenderJinja(env)
    assert document.content != 'rendered template'
    render([document])
    assert document.content == 'rendered template'
    assert template.mock_calls == [mock.call.render(document.metadata)]


def test_document_page_transform(document):
    page = frelia.page.Page('foo', document)
    document_func = mock.Mock()
    page_func = frelia.transforms.DocumentPageTransform(document_func)
    page_func([page])
    positional_args = document_func.call_args[0]
    assert list(positional_args[0]) == [document]


def test_rebase_page_path(page):
    page.path = 'root/blog/post'
    transform = frelia.transforms.RebasePagePath('root')
    transform([page])
    assert page.path == 'blog/post'


def test_strip_page_extension_path_html(page):
    page.path = 'blog/post.html'
    frelia.transforms.strip_page_extension([page])
    assert page.path == 'blog/post'


def test_strip_page_extension_path_index_html(page):
    page.path = 'blog/index.html'
    frelia.transforms.strip_page_extension([page])
    assert page.path == 'blog/index.html'


def test_strip_page_extension_path_nonhtml(page):
    page.path = 'static/style.css'
    frelia.transforms.strip_page_extension([page])
    assert page.path == 'static/style.css'


@pytest.fixture
def template():
    template = mock.create_autospec(jinja2.Template, instance=True)
    template.render.return_value = 'rendered template'
    return template


@pytest.fixture
def env(template):
    env = mock.create_autospec(jinja2.Environment, instance=True)
    env.from_string.return_value = template
    return env
