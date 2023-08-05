from setuptools import setup, find_packages


setup(
    name="buildkite-log-parse",
    version="1.0.1",
    description=("Parse orgs pipelines for active build/job and parse string"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="buildkite-log-parse",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["requests"],
    test_suite="tests",
    entry_points={
        "console_scripts": ["buildkite-log-parse=buildkite_log_parse.main:main"]
    },
)
