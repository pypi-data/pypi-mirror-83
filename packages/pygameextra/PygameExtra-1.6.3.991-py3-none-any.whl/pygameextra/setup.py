from setuptools import setup, find_packages
print('===setup PGE===')
setup(
    packages=find_packages(include=['bin/*']),
    scripts=['examples/pong/pygameextra-pong']
)
