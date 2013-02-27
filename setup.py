from setuptools import setup

setup(
    name="djunk_drawer",
    author="Jon Smajda",
    author_email="jon@smajda.com",
    description="Yet another grab bag of reusable Django stuff",
    version="0.1",
    packages=['djunk_drawer'],
    install_requires=[
        "django >= 1.4",
        "markdown",
        "mdx-smartypants",
        "python-dateutil",
        "tablib",
    ],
)
