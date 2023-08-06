from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='black-box-package',
    version='0.0.1',
    url='https://bitbucket.org/ainstec/black-box-package',
    license='MIT License',
    author='Ravi Jose Fiori',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ravi.fiori@concil.com.br',
    keywords='Pacote',
    description=u'Exemplo de pacote PyPI',
    packages=['black-box-package'],
    package_dir={'black-box-package': '.',},
    install_requires=['boto3', 'pandas', 'numpy', 'pyarrow', 'SQLAlchemy', 'psycopg2', 'psycopg2-binar', 'workalendar', 'cx-Oracle'],
)