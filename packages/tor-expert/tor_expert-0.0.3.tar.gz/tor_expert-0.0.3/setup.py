from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='tor_expert',
      version='0.0.3',
      description='Using tor expert as service',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Dragan Matesic',
      author_email='dragan.matesic@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=['requests', 'bs4', 'lxml', 'html5lib', 'stem', 'psutil', 'pysocks'],
       )
