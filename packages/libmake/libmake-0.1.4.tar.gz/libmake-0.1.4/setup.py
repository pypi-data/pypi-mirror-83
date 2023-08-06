# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# write version on the fly - inspired by numpy
MAJOR = 0
MINOR = 1
MICRO = 4
ISRELEASED = True
SHORT_VERSION = "%d.%d" % (MAJOR, MINOR)
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)


def write_version_py(filename="src/libmake/version.py"):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
major = %(major)d
short_version = '%(short_version)s'
version = '%(version)s'
full_version = '%(full_version)s'
is_released = %(isreleased)s
"""
    FULLVERSION = VERSION
    if not ISRELEASED:
        FULLVERSION += "-develop"

    a = open(filename, "w")
    try:
        a.write(
            cnt
            % {
                "major": MAJOR,
                "short_version": SHORT_VERSION,
                "version": VERSION,
                "full_version": FULLVERSION,
                "isreleased": str(ISRELEASED),
            }
        )
    finally:
        a.close()


def setup_package():
    # write version
    write_version_py()
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="libmake",
        version=VERSION,
        description="Building blocks make-like utils",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="A.Candido",
        author_email="candido.ale@gmail.com",
        url="https://github.com/AleCandido/libmake.py",
        package_dir={"": "src"},
        packages=find_packages("src"),
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ],
        install_requires=[],
        setup_requires=["wheel"],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    setup_package()
