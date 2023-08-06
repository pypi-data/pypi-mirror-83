from setuptools import setup, find_packages
print('===setup PGE===')
setup(
    name=pygameextra-pong
    packages=find_packages(include=['pygameextra-pong,bin/*']),
    scripts=['examples/pong/pygameextra-pong']
)
