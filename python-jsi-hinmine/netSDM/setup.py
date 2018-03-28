from setuptools import setup

setup(
    name='cf_netSDM',
    install_requires=['numpy==1.14.2', 'rdflib>=4.2.2'],
    version='0.0.2',
    license='MIT License',
    description='ClowdFlows module for network analysis for semantic data mining',
    author='Jan Kralj',
    author_email='jan.kralj@ijs.si',
    packages=['cf_netSDM', ],
    classifiers= ['Development Status :: 2 - Pre-Alpha',
                  'Environment :: Web Environment',
                  'Framework :: Django',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: MIT License',
                  'Operating System :: OS Independent',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  ],
    include_package_data=True,
)
