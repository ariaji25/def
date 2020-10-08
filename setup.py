from setuptools import setup

setup(
    name='directional_feature',
    version='0.1.0',    
    description='A Algorithm for image feature extraction',
    url='https://github.com/ariaji25/def',
    author='Ari Purnama Aji',
    author_email='ari.purnama838@gmail.com',
    packages=['directional_feature'],
    install_requires=['opencv-python',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)