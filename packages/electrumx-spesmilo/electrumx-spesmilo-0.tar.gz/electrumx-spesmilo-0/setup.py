import setuptools

version = '0'

setuptools.setup(
    name='electrumx-spesmilo',
    version=version,
    packages=setuptools.find_packages(include=('electrumx*',)),
    description='ElectrumX Server',
    author='Electrum developers',
    author_email='electrumdev@gmail.com',
    license='MIT Licence',
    url='https://github.com/spesmilo/electrumx',
    long_description='Server implementation for the Electrum protocol',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        "Programming Language :: Python :: 3",
    ],
)
