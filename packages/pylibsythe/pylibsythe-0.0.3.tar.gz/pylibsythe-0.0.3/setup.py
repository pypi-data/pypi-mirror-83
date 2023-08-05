from setuptools import setup, find_namespace_packages

name = "pylibsythe"


def long_description():
    with open("README.md") as fp:
        return fp.read()


setup(
    name="pylibsythe",
    version="0.0.3",
    description="pylibsythe",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="tandemdude",
    author_email="tandemdude1@gmail.com",
    url="https://gitlab.com/tandemdude/pylibsythe",
    packages=find_namespace_packages(include=[name + "*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8.3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
