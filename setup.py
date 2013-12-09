import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command import egg_info

packageName = "merlyn"

import re
versionLine = open("{0}/_version.py".format(packageName), "rt").read()
match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionLine, re.M)
versionString = match.group(1)

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        sys.exit(tox.cmdline([]))

def _topLevel(name):
    return name.split('.', 1)[0]

def _hacked_write_toplevel_names(cmd, basename, filename):
    names = map(_topLevel, cmd.distribution.iter_distribution_names())
    pkgs = dict.fromkeys(set(names) - set(["twisted"]))
    cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

egg_info.write_toplevel_names = _hacked_write_toplevel_names

setup(name=packageName,
      version=versionString,
      description='A server backend for interactive online exercises.',
      long_description=open("README.rst").read(),
      url='https://github.com/crypto101/' + packageName,

      author='Laurens Van Houtven',
      author_email='_@lvh.io',

      packages=find_packages() + ['twisted.plugins'],
      test_suite=packageName + ".test",
      setup_requires=['tox'],
      cmdclass={'test': Tox},
      zip_safe=True,

      license='ISC',
      keywords="crypto twisted",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Framework :: Twisted",
          "Intended Audience :: Education",
          "License :: OSI Approved :: ISC License (ISCL)",
          "Programming Language :: Python :: 2 :: Only",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Education",
          "Topic :: Games/Entertainment",
          "Topic :: Security :: Cryptography",
        ]
)

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
