from setuptools import setup

from roboversion import get_version


with open('README.md') as readme:
	long_description = readme.read()


setup(
	name='phantom-action-handler',
	version=str(get_version(alpha_branch='alpha')),
	packages=['phantom_dev.action_handler'],
	author='David Finn',
	author_email='dfinn@splunk.com',
	description='Utilities to simplify Phantom app development',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://gitlab.com/phantom6/phantom-action-handler',
	python_requires='>=3.6',
)
