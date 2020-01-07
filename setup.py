# To upload the latest version, change "version=0.X.X+1" and type:
# python setup.py sdist upload


from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pydivide',
      version='0.2.13',
      description='A tool to plot MAVEN data',
      url='http://github.com/MAVENSDC/pydivide',
      author='MAVEN SDC',
      author_email='mavensdc@lasp.colorado.edu',
      license='MIT',
      keywords='tplot maven mars lasp idl divide spedas',
      packages=['pydivide'],
      install_requires=['pytplot', 'pyspedas'],
      include_package_data=True,
      zip_safe=False)
