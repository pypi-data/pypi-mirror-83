import setuptools

setuptools.setup(
    name='libplot',
    version='0.5.0',
    author='Antony B Holmes',
    author_email='antony.b.holmes@gmail.com',
    description='A library for creating beautiful plots.',
    url='https://github.com/antonybholmes/libplot',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
