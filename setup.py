from setuptools import setup, find_packages

extras_require = {
    'XMLRenderer': [
        'lxml >= 2.3, < 4',
    ],
    'Serial': [
        'pyserial',
    ],
}

setup(
    name='linemode',
    url='github.com/bwhmather/python-linemode',
    version='0.1.0',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='BSD',
    description='Drivers and templates for thermal printers',
    long_description=__doc__,
    install_requires=[
    ],
    extras_require=extras_require,
    tests_require=list(set(sum(
        (extras_require[extra] for extra in ['XMLRenderer']), []
    ))),
    packages=find_packages(),
    package_data={
        '': ['*.*'],
    },
    zip_safe=False,
    test_suite='linemode.tests.suite',
)
