from setuptools import setup

# TODO: add other info (version, author, etc.)
setup(
    name='stack',
    packages=['persisted'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
