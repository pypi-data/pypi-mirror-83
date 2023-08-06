import setuptools

setuptools.setup(
    name='libcluster',
    version='0.5.0',
    author='Antony B Holmes',
    author_email='antony.b.holmes@gmail.com',
    description='A library creating cluster plots.',
    url='https://github.com/antonybholmes/libcluster',
    packages=setuptools.find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
