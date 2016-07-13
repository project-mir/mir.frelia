"""Document renderers.

Document renderers are callables that take a document object and returns some
kind of rendered output.

"""


class JinjaDocumentRenderer:

    """Render documents using Jinja.

    Documents have the metadata and content attributes.

    """

    def __init__(self, env, default_template='base.html'):
        self.env = env
        self.default_template = default_template

    def __call__(self, document):
        """Render document."""
        template = self._get_template(document)
        context = self._get_context(document)
        return template.render(context)

    @staticmethod
    def _get_context(document):
        """Get context for rendering document."""
        context = document.metadata.copy()
        context['content'] = document.content
        return context

    def _get_template(self, document):
        """Get Jinja template for document."""
        template_name = self._get_template_name(document)
        return self.env.get_template(template_name)

    def _get_template_name(self, document):
        return document.metadata.get('template', self.default_template)