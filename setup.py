import os
import sys

from setuptools import setup
from setuptools.command.install import install

BASE_DIR = os.path.dirname(__file__)

ABOUT = dict()
with open(os.path.join(BASE_DIR, "constant_sorrow", "__about__.py")) as f:
    exec(f.read(), ABOUT)


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != ABOUT['__version__']:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, ABOUT['__version__']
            )
            sys.exit(info)


INSTALL_REQUIRES = ['bytestringsplitter']
EXTRAS_REQUIRE = {'testing': ['bumpversion'],
                  'docs': ['sphinx', 'sphinx-autobuild']}

setup(name=ABOUT['__title__'],
      url=ABOUT['__url__'],
      version=ABOUT['__version__'],
      author=ABOUT['__author__'],
      author_email=ABOUT['__email__'],
      description=ABOUT['__summary__'],
      extras_require=EXTRAS_REQUIRE,
      install_requires=INSTALL_REQUIRES,
      packages=['constant_sorrow'],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Natural Language :: English",
          "Programming Language :: Python :: Implementation",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      python_requires='>=3',
      cmdclass={'verify': VerifyVersionCommand}
      )
