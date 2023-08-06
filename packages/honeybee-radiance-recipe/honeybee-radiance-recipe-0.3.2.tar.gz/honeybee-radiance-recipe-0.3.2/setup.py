import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="honeybee-radiance-recipe",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Collection of recipes for running daylight studies using honeybee-radiance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/honeybee-radiance-recipe",
    packages=setuptools.find_packages(exclude=["tests*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent"
    ],
    license="AGPL-3.0"
)
