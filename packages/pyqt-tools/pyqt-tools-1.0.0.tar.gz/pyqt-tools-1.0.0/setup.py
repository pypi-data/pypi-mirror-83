from setuptools import setup, find_packages

setup(
    name = 'pyqt-tools',
    packages = find_packages(),
    platform=['any'],
    version = '1.0.0',
    author = 'David Roman',
    author_email = 'davidroman96@gmail.com',
    url = 'https://github.com/IFAEcontrol/pyqt-tools',
    license = 'BSD-3',
    install_requires=[
        'guiqwt',
        'numpy',
        'PyQt5',
    ],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 3'
	],
)
