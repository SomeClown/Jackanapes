from setuptools import setup, find_packages

setup(
        name='CloudSackedTweets',
        version='0.1',
        packages=find_packages(),
        include_pacakge_date=True,
        install_requires=[
            'Click',
            'tweepy',
            ],
        entry_points='''
        [console_scripts]
        CloudSackedTweets=CloudSackedTweets.__init__:cli
        ''',
        )
