{
    'build-system': {
        'requires': [
            'setuptools>=61.0'
        ],
        'build-backend': 'setuptools.build_meta'
    },
    'project': {
        'name': 'GailBot',
        'license': {
            'file': 'LICENSE'
        },
        'description': 'An Automated Transcription System for Conversation Analysis',
        'maintainers': [
            {
                'name': 'Human Interaction Lab - Tufts University',
                'email': 'hilab-dev@elist.tufts.edu'
            }
        ],
        'requires-python': '>=3.8',
        'dependencies': [
            'pydub',
            'sounddevice',
            'moviepy',
            'dacite',
            'networkx',
            'ibm_watson',
            'scipy',
            'syllables',
            'pyyaml',
            'lxml'
        ],
        'readme': 'README.md',
        'classifiers': [
            'Intended Audience :: Science/Research',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Topic :: Scientific/Engineering',
            'Operating System :: MacOS'
        ],
        'dynamic': [
            'version'
        ],
        'optional-dependencies': {
            'test': [
                'pytest',
                'pytest-cov',
                'pytest-timeout',
                'pytest-xdist'
            ]
        },
        'urls': {
            'homepage': 'https://github.com/mumair01/GailBot',
            'source': 'https://github.com/mumair01/GailBot',
            'download': 'https://github.com/mumair01/GailBot/releases',
            'tracker': 'https://github.com/mumair01/GailBot/issues'
        }
    },
    'tool': {
        'setuptools': {
            'packages': {
                'find': {
                    'where': [
                        '.'
                    ]
                }
            },
            'dynamic': {
                'version': {
                    'attr': 'gailbot.__version__'
                }
            }
        },
        'pytest': {
            'ini_options': {
                'minversion': '6.0',
                'addopts': '-ra -q',
                'testpaths': [
                    'tests'
                ],
                'filterwarnings': [
                    'ignore::DeprecationWarning'
                ]
            }
        }
    }
}