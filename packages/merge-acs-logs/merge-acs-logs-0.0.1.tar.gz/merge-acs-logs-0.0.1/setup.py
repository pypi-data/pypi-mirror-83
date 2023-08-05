from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="merge-acs-logs",
    version="0.0.1",
    description="just a small tool to merge log files of ACS by timestamp",
    long_description=long_description,
    url="https://github.com/dneise/merge_acs_logs",
    author="Dominik Neise",
    author_email="neised@phys.ethz.ch",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["docopt", "iso8601", "tqdm"],
    entry_points={"console_scripts": ["merge_acs_logs = merge_acs_logs:main"]},
)
