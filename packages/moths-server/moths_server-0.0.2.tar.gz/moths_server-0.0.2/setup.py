from setuptools import setup, find_packages

setup(name="moths_server",
      version="0.0.2",
      description="messenger_project_server",
      author="Fedor Kleshchev",
      author_email="f.kleshev@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'threading'])
