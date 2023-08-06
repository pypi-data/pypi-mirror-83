import setuptools

setuptools.setup(
    name='libtsne',
    version='0.4.0',
    author='Antony B Holmes',
    author_email='antony.b.holmes@gmail.com',
    description='A library for creating t-sne plots',
    url='https://github.com/antonybholmes/libtsne',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
