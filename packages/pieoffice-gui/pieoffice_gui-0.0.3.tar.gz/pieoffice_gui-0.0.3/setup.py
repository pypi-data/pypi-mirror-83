from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="pieoffice_gui",
        description="A GUI script converter for ancient (Proto-)Indo-European languages based on pieoffice.",
        url="https://gitlab.com/caiogeraldes/pieoffice_gui",
        long_description=long_description,
        long_description_content_type="text/markdown",
        version="0.0.3",
        license="MIT",
        author="Caio Geraldes",
        author_email="caiogeraldes@protonmail.com",
        packages=find_packages(),
        entry_points={
        'console_scripts': [
           'pieoffice_gui=pieoffice_gui.__main__:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=['betacode', 'pieoffice', 'pygtrie', 'PySide2'],
        python_requires=">=3.6",
)
