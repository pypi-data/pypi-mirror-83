from setuptools import setup, find_packages

setup(
    name='url2',
    version='1.0',
    description=(
        'Crawler series tool set.'
    ),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='zkung',
    author_email='du163455@gmail.com',
    maintainer='zkung',
    maintainer_email='du163455@gmail.com',
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/zkung/url2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
    ],
)
