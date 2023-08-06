from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='black-box-package',
    version='0.0.2',
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
    install_requires=['boto3==1.11.0', 'pandas==0.25.1', ' numpy==1.16.5', 'pyarrow==0.15.1', 'SQLAlchemy==1.3.15', 'psycopg2==2.8.4', 'psycopg2-binary==2.8.5', 'workalendar==10.4.0', 'cx-Oracle==8.0.1'],
)


# cria a pasta dist com o pacote
#python setup.py sdist bdist_wheel

# subir no ambiente de teste 
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# subir no pipy
#twine upload dist/*


#install
#pip install black-box-package==0.0.1