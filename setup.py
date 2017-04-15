from setuptools import setup, find_packages

setup(
        name='jackanapes',
        version='0.1a0',
        description='twitter utilities client',
        url='https://github.com/SomeClown/PQ',
        license='MIT',
        author='@someclown',
        author_email='teren@packetqueue.net',
        packages=find_packages(),
        install_requires=[
            'tweepy',
            'click',
            'progressbar2',
            'pyyaml',
            ],
        entry_points = {
            'console_scripts': ['jackanapes=app.jack:cli'],
            }
        )
