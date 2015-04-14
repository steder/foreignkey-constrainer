from setuptools import setup, find_packages

setup(
    name="foreignkey-constrainer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy==0.9.9',
        'psycopg2==2.6'
    ],
    scripts=['bin/add-constraints'],
    url="https://github.com/steder/foreignkey-constrainer",
)
