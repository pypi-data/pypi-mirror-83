from setuptools import setup


setup(
    name='simple_qiwi',
    version='0.8',
    author='protectedsnow',
    description='QIWI API for Humans',
    long_description='See https://github.com/protectedsnow/simple_qiwi',
    url='https://github.com/protectedsnow/simple_qiwi',
    install_requires=['requests', 'uuid', 'flask'],
    packages=['simple_qiwi']
)