from distutils.core import setup

setup(
    name='CloudSackedTweets',
    version='0.1a0',
    packages=[''],
    package_dir={'': 'app'},
    url='https://github.com/SomeClown/PQ',
    license='MIT',
    author='@someclown',
    author_email='teren@packetqueue.net',
    description='twitter utilities client',
    entry_points='''
    [console_scripts]
    CloudSackedTweets=pq:cli
    ''', requires=['click', 'progressbar', 'tweepy', 'yaml']
)
