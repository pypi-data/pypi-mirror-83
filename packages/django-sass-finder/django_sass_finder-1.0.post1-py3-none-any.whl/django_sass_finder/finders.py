from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.core.checks import Error
import sass

class ScssFinder(BaseFinder):
    """
    Finds .scss files specified in SCSS_ROOT and SCSS_COMPILE settings.
    """

    def __init__(self, *_args, **_kwargs):
        try:
            self.scss_compile = settings.SCSS_COMPILE
        except AttributeError:
            self.scss_compile = []
        self.root = settings.SCSS_ROOT
        self.storage = FileSystemStorage(settings.CSS_COMPILE_DIR)

    def check(self, **kwargs):
        """
        Checks if ScssFinder is configured correctly.

        SCSS_COMPILE should contain valid files.
        """
        errors = []

        for scss_item in self.scss_compile:
            abspath = self.root / scss_item
            if not abspath.exists() and not abspath.is_file():
                errors.append(Error(
                    f'{scss_item} is not a valid file.',
                    id='sass.E001'
                ))
        return errors

    def find(self, path, all=False):
        """
        Look for files in SCSS_ROOT, and make their paths absolute.
        """
        if all:
            return str([settings.CSS_COMPILE_DIR / path])
        return str(settings.CSS_COMPILE_DIR / path)

    def list(self, _ignore_patterns):
        """
        Compile then list the .css files.
        """
        for scss_item in self.scss_compile:
            abspath = self.root / scss_item
            if abspath.is_file():
                abspath = self.root / scss_item
                abspath_str = str(abspath)
                outpath = settings.CSS_COMPILE_DIR / (abspath.stem + '.css')
                with open(outpath, 'w+') as outfile:
                    outfile.write(sass.compile(filename=abspath_str, output_style='compressed'))
                print(settings.BASE_DIR)
                yield abspath.stem + '.css', self.storage
