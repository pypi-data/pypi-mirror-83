from setuptools import setup

setup(name='ripplepy',
    version='0.1',
    description='RipplePy is a osu!ripple third party API',
    long_description="RipplePy is a osu!ripple third party API written in Python by NateTH. Easy to use and have performance",
    url='https://github.com/kidJaNateTH/ripplepy',
    author='NateTH',
    author_email='kidjanate@gmail.com',
    license='NateTH',
    install_requires=[
    ],
    scripts=['bin/status.py'],
    keywords='RipplePy',
    packages=['ripplepy'],
    package_dir={'ripplepy': 'src/ripplepy'},
    package_data={'ripplepy': ['file/*.py']}
)