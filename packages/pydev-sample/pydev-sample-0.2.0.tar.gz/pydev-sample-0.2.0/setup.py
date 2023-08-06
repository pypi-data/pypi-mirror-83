import setuptools

setuptools.setup(
    name='pydev-sample',
    version='0.2.0',
    description='Sample package to illustrate Python development.',
    author='Neal Morton',
    author_email='mortonne@gmail.com',
    license='GPLv3',
    url='http://github.com/mortonne/pydev_sample',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    scripts=[
        'scripts/compare_cities',
        'scripts/city_summary',
    ],
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'wikipedia',
        'tensorflow',
        'tensorflow_hub',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
    ]
)
