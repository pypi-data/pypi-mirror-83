from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/coblack"

with open("ReadMe.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="coblack",
    description="Black-compliant formatter/rewrapper for Python comments.",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">= 3.8",  # For the `importlib` package used in __init__.py.
    install_requires=[
        "click ~= 7.1",  # black depends on "click>=7.1.2". ✔
        "black >= 20",  # black uses calendar versioning (i.e. this means "a version from 2020 or later"). No idea if a later version
        #               # will break the current API we use, but oh well, we'll hear
        #               # about it then.
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},  # This means: "Root package can be found in 'src' dir"
    entry_points={"console_scripts": ["coblack = coblack.format_file:cli"]},
    # Get package version from git tags
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
)
