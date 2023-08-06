from setuptools import setup

setup(
    name='ciscoglass',
    version='0.1.3',
    description='Wrapper/SDK for Cisco Glass Apps',
    url='https://wwwin-github.cisco.com/ciscoglass/python-sdk.git',
    author='Adyanth H',
    author_email='adyah@cisco.com',
    # license='BSD 2-clause',
    packages=['ciscoglass'],
    install_requires=['requests'],

    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Intended Audience :: Science/Research',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.8',
    ],
)