from setuptools import setup

setup(
    name="torrench",
    version="1.0.0",
    description="A powerful multi-site torrent search tool for the command line",
    author="Mahmoud Almezali",
    author_email="mzmcsmzm@gmail.com",
    url="https://github.com/almezali/enhanced-torrench",
    py_modules=['torrench'],  
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
        "tabulate>=0.8.0",
        "termcolor>=1.1.0"
    ],
    entry_points={
        'console_scripts': [
            'torrench=torrench:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6"
)

