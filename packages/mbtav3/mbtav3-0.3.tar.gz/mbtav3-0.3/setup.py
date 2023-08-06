from setuptools import setup, find_packages

setup(
    name='mbtav3',
    version='0.3',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/djsv23/mbtav3',
    license='MIT',
    author='Daniel Steiner',
    author_email='djsteiner93@gmail.com',
    description='Python library for MBTA v3 realtime API',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'aiohttp'
    ]
)
