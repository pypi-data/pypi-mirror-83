import setuptools

version = '0'

setuptools.setup(
    name='aiorpcx-spesmilo',
    version=version,
    packages=['aiorpcx'],
    description='Generic async RPC implementation, including JSON-RPC',
    author='Electrum developers',
    author_email='electrumdev@gmail.com',
    license='MIT Licence',
    url='https://github.com/spesmilo/aiorpcx',
    long_description=(
        'Transport, protocol and framing-independent async RPC '
        'client and server implementation.  '
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
    ],
)
