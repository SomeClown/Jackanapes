from setuptools import setup, find_packages

setup(
    name='CloudSackedTweets',
    version='.01',
    packages=find_packages(),
    include_pacakge_date=True,
    url='https://github.com/SomeClown/PQ',
    license='MIT',
    author='@someclown',
    author_email='teren@packetqueue.net',
    description='Command line twitter utility',
    install_requires=[
        'Click',
        'tweepy',
        ],
        entry_points='''
        [console_scripts]
        CloudSackedTweets=CloudSackedTweets.__init__:cli
        ''',
        )
