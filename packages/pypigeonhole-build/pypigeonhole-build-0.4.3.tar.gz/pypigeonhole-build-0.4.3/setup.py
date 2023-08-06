from setuptools import setup, find_packages
import pathlib
import sys
import os.path
from os.path import dirname

# To add source folder to the path, otherwise below import would fail.
src_path = os.path.join(dirname(__file__), 'src')
sys.path.append(src_path)

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

from pypigeonhole_build import app_setup
from pypigeonhole_build import dep_setup

# If this is needed during dev by others, cd this folder and run pip install -e .
# This is reusable in normal cases.
setup(name=app_setup.get_app_name(),
      version=app_setup.get_app_version(),  # major.minor.patch
      description='Python build & packaging tool',
      url='https://github.com/psilons/pypigeonhole-build',

      author='psilons',
      author_email='psilons.quanta@gmail.com',

      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT",

      package_dir={'': 'src'},
      # setup complains last ".", but it works to include top des_setup.py
      # not needed anymore
      # packages=find_packages("src", exclude=["test"]) + ['.'],
      packages=find_packages("src", exclude=["test"]),

      python_requires=dep_setup.python_required if dep_setup.python_required else '>=3',

      install_requires=dep_setup.install_required,

      tests_require=dep_setup.test_required,

      extras_require={},
      )

# To test: 3 cases
#     python setup.py install
#     pip install . -t <target dir>
#         make sure there is no egg-info folder here, otherwise error with no
#         .egg file found, thought the package is installed successfully.
#     python -m pip install . --no-deps --ignore-installed -vv
