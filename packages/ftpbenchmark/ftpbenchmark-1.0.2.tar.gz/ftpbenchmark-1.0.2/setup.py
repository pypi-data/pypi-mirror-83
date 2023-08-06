from setuptools import setup

setup(
    name="ftpbenchmark",
    version="1.0.2",
    packages=["ftpbenchmark"],
    url="http://github.com/imjoseangel/ftpbenchmark",
    license="MIT",
    author="Jose Angel Munoz",
    author_email="josea.munoz@gmail.com",
    description="Benchmark for ftp servers",
    long_description=open("README").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Console :: Framebuffer",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: System :: Benchmark",
        "Topic :: Utilities",
    ],
    install_requires=[
        "setuptools", "gevent", "dnspython", "Timecard"
    ],
    entry_points={
        "console_scripts": ["ftpbenchmark = ftpbenchmark.ftpbenchmark:main"]
    }
)
