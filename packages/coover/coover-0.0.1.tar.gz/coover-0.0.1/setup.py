import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="coover",
	version="0.0.1",
	author="coverosu",
	author_email="ImEasyCJ@gmail.com", # cringe!
	description="Using this package for code that I tend to rewrite a lot",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/coverosu/coverosu_pkg",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)