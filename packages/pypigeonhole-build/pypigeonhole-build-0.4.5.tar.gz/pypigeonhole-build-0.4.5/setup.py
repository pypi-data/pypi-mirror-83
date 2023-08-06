from setuptools import setup, find_packages
import pathlib
import os
import sys

import pypigeonhole_build.app_setup as app_setup

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


# If this is needed during dev by others, cd this folder and run pip install -e .
# This is reusable in normal cases.
setup(name=app_setup.app_name(),
      version=app_setup.app_version(),  # major.minor.patch
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

      python_requires=app_setup.python_required,

      install_requires=app_setup.install_required,

      tests_require=app_setup.test_required,

      extras_require={},
      )
