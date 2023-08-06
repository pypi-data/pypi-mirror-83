from setuptools import setup,find_packages, os

setup(
    name='run-fargate-task',
    version="1.0.0",
    description='Script to trigger fargate tasks',
    url='https://github.com/redaptiveinc/devops-scripts',
    author='Mariano Gimenez',
    author_email='mariano.gimenez@agileengine.com',
    license='unlicense',
    zip_safe=False,
    packages=find_packages(),
    entry_points ={
        'console_scripts': [
            'run-task = src.main:main'
        ]
    },
    install_requires = [
        'python-dotenv==0.10.3',
        'boto3==1.10.7',
    ]
)
