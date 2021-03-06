from setuptools import setup, find_packages

setup(
    name='easytextgen',
    version='1.1',
    description='API to work with transformer based text generation engines and creating prompts.',
    packages=find_packages(),
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