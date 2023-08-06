from setuptools import setup

setup(
    name='jsonparserdf',
    version='0.0.1',
    description = 'Process json and convert it into dataframes',
    py_modules=["jsonparserdf"],
    package_dir={'':'src'},
    install_requires = [
        'pandas ~= 1.1.3',
        'XlsxWriter ~= 1.3.7'

    ],
    url='https://github.com/NabeelZaidi',
    author='Nabeel Zaidi',
    author_email='nabeel.zaidi@lyftron.com'
    
)