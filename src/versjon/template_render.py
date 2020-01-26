import os
import jinja2


class TemplateRender(object):
    """ Finds the template on the file system with a given name. """

    def __init__(self, user_path):
        """ Create a new instance.
        :param user_path: The directory on the file system where the user
            provided templates are located as a string. If user_path is None
            no user specified templates will be loaded.
        """

        # We have two loaders either we load from the package
        # or from an user specified location
        loaders = []

        if user_path:
            assert os.path.isdir(user_path)

            loaders.append(
                jinja2.FileSystemLoader(searchpath=user_path))

        loaders.append(
            jinja2.PackageLoader(
                package_name='versjon', package_path='templates'))

        self.environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(loaders=loaders),
            trim_blocks=True,
            lstrip_blocks=True,
            # Enable the do statement:
            # https://stackoverflow.com/a/39858522/1717320
            extensions=['jinja2.ext.do'])

    def render(self, template_file, **kwargs):
        """ Render the template

        :param template_file: The filename of the template to render
        :param kwargs: Keyword arguments containing the context information
        """

        template = self.environment.get_template(name=template_file)
        return template.render(**kwargs)
