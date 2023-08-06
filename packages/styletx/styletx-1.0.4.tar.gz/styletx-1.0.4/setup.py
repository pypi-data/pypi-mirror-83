import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup (name = 'styletx',
    version = '1.0.4',
    description = 'Initial release with StyleTransfer',
    author = 'Dinesh Kumar Gnanasekaran',
    author_email = 'dinesh.gna111@gmail.com',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/dinesh-GDK/StyleTx",
    packages = ['styletx'],
    license = 'MIT',
    zip_safe = False,
    include_package_data=True,
    python_requires = '>3.8',
)