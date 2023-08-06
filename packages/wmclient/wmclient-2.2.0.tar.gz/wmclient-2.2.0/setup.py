import setuptools

with open('README') as f:
    long_description = f.read()

setuptools.setup(
    name='wmclient',
    packages=['wmclient'],
    version='2.2.0',
    license='apache-2.0',
    description='WURFL Microservice client for Python',
    long_description=long_description,
    author='Scientiamobile Inc.',
    author_email='support@scientiamobile.com',
    url='https://github.com/WURFL/wurfl-microservice-client-python',
    keywords=['device', 'mobile', 'device detection', 'analytics'],
    install_requires=[
        'pycurl',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
