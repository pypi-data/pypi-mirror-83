from setuptools import setup

classifiers = [
	"Programming Language :: Python :: 3.8"
]

setup(
	name="discordce",
	description="Append .png to cached discord data files.",
	long_description="Read more at https://github.com/Slyyxp/Discord-Cache-Exporter",
	url="https://github.com/Slyyxp/Discord-Cache-Exporter",
	author="Slyyxp",
	author_email="slyyxp@protonmail.com",
	classifiers=classifiers,
	version="0.1",
	packages=['discordce'],
	entry_points={
		'console_scripts': [
			'discordce = discordce.__main__:main'
		]
	})
