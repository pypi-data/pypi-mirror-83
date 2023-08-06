from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'typeshell',
    version = '0.1.0',
    author='Greyson Murray',
    author_email='greysonmurray.dev@gmail.com',
    description='Typing test CLI tool.',
    long_description=long_description,
	long_description_content_type="text/markdown",
    url='https://github.com/greysonDEV/typeshell-cli',
    license='MIT',
    classifiers = [
    	"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.8",
		"Topic :: Games/Entertainment",
		"Operating System :: MacOS",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Natural Language :: English"
    ],
    python_requires='>=3.8',
    install_requires=[
    	'pytyper'
    ],
    include_package_data=True,
    packages = ['typeshell'],
    entry_points = {
        'console_scripts': [
            'typeshell = typeshell.__main__:main'
        ]
    })