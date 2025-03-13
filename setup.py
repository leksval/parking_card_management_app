from setuptools import setup, find_packages

setup(
    name="parking_card_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'sqlalchemy>=1.4.0',
    ],
)
