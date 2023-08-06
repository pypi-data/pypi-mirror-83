import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


project_urls = {
    'Source Code':      'https://github.com/bicarlsen/sphinx-bootstrap',
    'Bug Tracker':      'https://github.com/bicarlsen/sphinx-bootstrap/issues'
}


setuptools.setup(
    name = "bric_sphinx_bootstrap",
    version = "0.0.1",
    author = "Brian Carlsen",
    author_email = "carlsen.bri@gmail.com",
    description = "Sphinx roles for Bootstrap elelments.",
    long_description = long_description,
    long_description_content_type = "text/x-rst",
    keywords = [ 'sphinx', 'rst', 'restructured text', 'bootstrap' ],
    url = "",
    project_urls = project_urls,
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    install_requires = [ 'docutils', 'Sphinx' ]
)