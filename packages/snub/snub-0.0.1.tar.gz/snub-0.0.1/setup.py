from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

setup(
    name='snub',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Snup is a python package to check IPs, Hashes, Emails, Domains, or URLs against blackhole lists and DNS services.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords='blackhole python api ip email hash domain url',
    url='https://github.com/swimlane/snub',
    author='Josh Rickard',
    author_email='josh.rickard@swimlane.com',
    package_data={
        'b':  ['data/*.yml']
    },
    entry_points={
          'console_scripts': [
              'snub = snub.__main__:main'
          ]
    }
)