from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-query-links",
    description="Turn SELECT queries returned by a query into links to execute them",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-query-links",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-query-links/issues",
        "CI": "https://github.com/simonw/datasette-query-links/actions",
        "Changelog": "https://github.com/simonw/datasette-query-links/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_query_links"],
    entry_points={"datasette": ["query_links = datasette_query_links"]},
    install_requires=["datasette>=0.59a1"],
    extras_require={"test": ["pytest", "pytest-asyncio", "beautifulsoup4"]},
    tests_require=["datasette-query-links[test]"],
    python_requires=">=3.6",
)
