from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3']
	
setup(
	name='NHL_API_Wrapper',
	version='0.1',
	description='A wrapper for the NHL API',
	long_description=open('README.txt').read()+'\n\n' + open('CHANGELOG.txt').read(),
	url='',
	author='Peter Faulkner',
	author_email='faulknep@yahoo.com',
	license='MIT',
	classifiers=classifiers,
	keywords=['nhl','nhl api','nhl api wrapper', 'hockey', 'stats'],
	packages=find_packages(),
	install_requires=['requests']
)