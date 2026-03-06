from setuptools import setup, find_packages

setup(
    name='eyes-socket',
    version='0.1.0',
    description='A persistency module for local bot persistency.',
    author='Jules',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'eyes-socket=eyes_socket.cli:main',
        ],
    },
    python_requires='>=3.6',
)
