import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'truncate-and-write-to-sql',
    version = '0.0.0',
    author = 'Markus Pettersen',
    author_email = 'mp.markus94@gmail.com',
    description = 'Truncate existing table and write to the table with new entries',
    long_description = long_description,
    url = 'https://github.com/MPettersen/truncate_and_write_to_sql',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.8',
)