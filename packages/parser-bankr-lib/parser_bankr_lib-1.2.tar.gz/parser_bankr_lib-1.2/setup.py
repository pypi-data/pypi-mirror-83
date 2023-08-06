from setuptools import setup


setup(
    name='parser_bankr_lib',
    version='1.2',
	install_requires=[
		'PyMySQL',
		'selenium',
		'configparser',
		'cryptography',
		'bs4'
	],
	packages=['parser_bankr_lib'],
)