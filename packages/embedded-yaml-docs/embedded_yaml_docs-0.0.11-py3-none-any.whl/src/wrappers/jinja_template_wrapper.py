from jinja2 import Environment, FileSystemLoader
from ..extensions.jinja_filters import JinjaFilters

class JinjaTemplateWrapper(Environment):
    """

    """


    def __init__(self, path: str, **kwargs):
        """

        """
        super().__init__(**kwargs)
        super().get_template(path)

        super.tests['contains'] = JinjaFilters.contains
        super.tests['startswith'] = JinjaFilters.startswith