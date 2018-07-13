from setuptools import find_packages, setup

setup(
    name='medtagger',
    version='0.0.1',
    packages=find_packages(exclude=['docs', 'backend', 'frontend']),
    include_package_data=True,
    py_modules=['cli'],
    description='Framework for annotating medical dataset',
    long_description='A collaborative framework for annotating medical datasets using crowdsourcing.',
    install_requires=[
        'click==6.7',
        'pyyaml==3.13',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    entry_points='''
        [console_scripts]
        medtagger=cli.__init__:cli
    ''',
)
