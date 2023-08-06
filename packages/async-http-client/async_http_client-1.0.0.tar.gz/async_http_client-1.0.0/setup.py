from setuptools import find_packages, setup

requirements = [
    'aiohttp==3.6.3'
]

setup(
    name='async_http_client',
    version='1.0.0',
    author="jaytarang92",
    author_email="jaytarang92@gmail.com",
    description='Async HTTP Client',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.5",
    packages=find_packages(exclude=[]),
    install_requires=requirements
)
