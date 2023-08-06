from setuptools import setup
setup(
    name='mavprint',
    version='0.1',
    packages=['mavprint'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="print mavlink messages to console",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="mavlink debug ardupilot",
    url="https://github.com/evidlo/mavprint",
    entry_points={
        'console_scripts': ['mavprint = mavprint.mavprint:main']
    },
    install_requires=[
        "pymavlink",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
