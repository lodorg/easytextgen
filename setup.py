from distutils.core import setup

setup(
    name='easytextgen',
    version='1.1',
    description='API to work with transformer based text generation engines and creating prompts.',
    packages=['easytextgen'],
    install_requires=[
        'openai',
        'attrs',
        'pydantic',
        'transformers',
        'requests',
        'rich',
        'pyyaml',
    ],
)