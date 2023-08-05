from jinja2 import Environment
from ..extensions.jinja_filters import JinjaFilters


class JinjaTemplateFactory():
    """

    """


    @staticmethod
    def create(path: str, **kwargs):
        """

        """
        environment = Environment(**kwargs)

        environment.tests['contains'] = JinjaFilters.contains
        environment.tests['startswith'] = JinjaFilters.startswith

        return environment.get_template(path)