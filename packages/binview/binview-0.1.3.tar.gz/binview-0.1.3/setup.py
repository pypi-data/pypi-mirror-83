from os.path import join, dirname, abspath

from setuptools import setup, find_packages


curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()


setup(
    name             = 'binview',
    version          = '0.1.3',
    description      = 'Binary Dumper',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://bitbucket.org/dugres/binview/src/stable/',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Testing',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3',
    ],
    package_dir = {
        'binview': 'binview',
    },
    packages = [
        'binview',
    ],
    entry_points = dict(
        console_scripts = (
            'binview=binview.cli:main',
        ),
    ),
)
