from setuptools import setup, find_packages

setup(
    name = 'gfagui',
    packages = find_packages(),
    platform=['any'],
    entry_points = {
        'console_scripts': ['gfagui=gfagui.main:main'],
    },
    version = '1.0.0',
    author = 'David Roman',
    author_email = 'droman@ifae.es',
    url = 'https://gitlab.pic.es/DESI-GFA/gfa_gui',
    license = 'BSD-3',
    install_requires=[
            'appdirs',
            'coloredlogs',
            'confuse',
            'gfaaccesslib',
            'gfafunctionality',
            'guiqwt',
            'PyQt5',
            'pyqt_tools',
        ],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 3'
	],
)
