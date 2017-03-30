from setuptools import setup

setup(
        name='CloudSackedTweets',
        version='0.1a0',
        description='twitter utilities client',
        url='https://github.com/SomeClown/PQ',
        license='MIT',
        author='@someclown',
        author_email='teren@packetqueue.net',
        packages=['app'],
        install_requires=[
            'tweepy',
            'click',
            'progressbar2',
            'pyyaml',
            ],
        entry_points = {
            'console_scripts': ['CloudSackedTweets=app.pq:cli'],
            }
        )
