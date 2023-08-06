import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="todoist_service",
    version="1.1",
    author="Tomer Rosenfeld",
    author_email="mail@tomerrosenfeld.com",
    description="Provide framework for Todoist 3rd party services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rosenpin/todoist-service",
    license="Unlicense",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "todoist",
        "flask",
        "tinydb",
        "requests-oauthlib"
    ],
    packages=[
        'todoist_service',
        'todoist_service.todoist_wrapper',
        'todoist_service.server.authorization',
    ],
    python_requires='>=3.8',
)
