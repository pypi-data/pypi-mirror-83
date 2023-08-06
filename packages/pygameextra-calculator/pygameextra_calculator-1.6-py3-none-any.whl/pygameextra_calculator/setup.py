from setuptools import setup, find_packages
print('===setup PGE===')
setup(
    name='pge-calculator',
    packages=find_packages(include=['scripts/pge-calculator,pge-calculator,bin/*']),
    scripts=['command/pge-calculator']
)
