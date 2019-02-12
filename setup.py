""" Install automechanic
"""
from distutils.core import setup


setup(name="automech",
      version="0.1.2",
      packages=["automechanic",
                "automechanic.task",
                "automechanic.parse",
                "automechanic.fs",
                "automechanic.fslib",
                "automechanic.tests"],
      scripts=["automech"],
      package_dir={'automechanic': "automechanic"},
      package_data={
          'automechanic': ["tests/data/heptane/*", "tests/data/natgas/*"]}
)
