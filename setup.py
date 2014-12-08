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
    version='0.2.0',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='BSD',
    description='Drivers and templates for thermal printers',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Printing',
    ],
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
