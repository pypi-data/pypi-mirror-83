from dominate.tags import p

from swole.widgets.base import Widget


class Markdown(Widget):
    """ A general widget to write Markdown. """
    def __init__(self, content="", **kwargs):
        """
        Arguments:
            content (`str`, optional): Markdown content. Defaults to empty string.
        """
        super().__init__(**kwargs)
        self.content = content

    def html(self):
        # TODO : Full markdown parsing + convertion to dominate tags
        return p(self.content, id=self.id)

    def get(self):
        return self.content

    def set(self, x):
        self.content = x
