import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ie-a-ia-io",     
    version="0.1.3",
    author="sgarda",
    author_email="samueleg.opt@posteo.us",
    description="Incredibly basic class for managing simple input/output streams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sgarda/ieaiaio_v1",
    packages=setuptools.find_packages(),
    classifiers=[
'Operating System :: OS Independent',
'Topic :: Utilities'],
    python_requires='>=3.5',
)
