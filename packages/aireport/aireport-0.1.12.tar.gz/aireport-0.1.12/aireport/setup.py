from setuptools import setup
from setuptools import setup, find_packages

setup(
    name="ProjectReportTools",
    version="",
    url="",
    license="",
    author="mjaquier",
    author_email="",
    description="Project Report Tools",
    entry_points='''[console_scripts]
                    ai=aireport:cli
                 ''',
    packages=find_packages(),
    include_package_data=True,
    keywords='report'
)
