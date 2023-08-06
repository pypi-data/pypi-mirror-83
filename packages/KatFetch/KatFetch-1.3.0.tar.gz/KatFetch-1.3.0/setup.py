"""
Setup
KatFetch installer
By Kat Hamer
"""

from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

with open("requirements.txt") as fp:
    requirements = fp.read().split("\n")

def main():
    """Main function"""
    setup(
        name="KatFetch",
        version="1.3.0",
        entry_points={"console_scripts": ["katfetch = katfetch.__main__:main"]},
        install_requires=requirements,
        packages=find_packages(),
        author="Katelyn Hamer",
        description="A minimal and customizable fetch script.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        keywords="fetch info system",
        url="https://gitlab.com/kathamer/katfetch",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Operating System :: POSIX :: Linux",
        ],
    )


if __name__ == "__main__":
    main()  # Run main function
