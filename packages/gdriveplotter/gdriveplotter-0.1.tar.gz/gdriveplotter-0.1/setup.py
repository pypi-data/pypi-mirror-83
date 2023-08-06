from setuptools import setup

with open("Readme.md", encoding='utf-8') as f:
    long_description = f.read()

setup(name = 'gdriveplotter',
      version = '0.1',
      description = 'Reads Gsheets from Gdrive and Plots graph',
      long_description = long_description,
      author = 'Akshay Mohite',
      packages = ["gdriveplotter"],
      install_requires=[
          'pandas','matplotlib','gspread',
      ],
      long_description_content_type='text/markdown')