from setuptools import setup, find_packages

setup(
    name='eyes-socket',
    version='0.1.0',
    description='A persistency module for local bot persistency.',
    author='Jules',
    packages=find_packages(),
    extras_require={
        'mcp': ['mcp>=1.0.0']
    },
    entry_points={
        'console_scripts': [
            'eyes-socket=eyes_socket.cli:main',
            'eyes-socket-mcp=eyes_socket.mcp_server:main',
        ],
    },
    python_requires='>=3.6',
)
