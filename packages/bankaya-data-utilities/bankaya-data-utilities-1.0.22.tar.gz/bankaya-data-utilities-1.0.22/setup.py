from setuptools import setup, find_packages

setup(name='bankaya-data-utilities',
      version='1.0.22',
      url='https://bitbucket.org/bankaya-dev/data-utilities',
      license='Bankaya',
      author='Enrique Garcia',
      author_email='enrique@bankaya.com.mx',
      description='Driver for data access utilities',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)