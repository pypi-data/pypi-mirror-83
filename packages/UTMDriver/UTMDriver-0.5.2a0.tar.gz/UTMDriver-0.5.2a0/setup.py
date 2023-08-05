from setuptools import setup, find_packages
import UTMDriver

setup(
    name='UTMDriver',
    install_requires=[
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'decorator==4.4.2',
        'idna==2.10',
        'Jinja2==2.11.2',
        'lxml==4.5.2',
        'MarkupSafe==1.1.1',
        'requests==2.24.0',
        'urllib3==1.25.10',
    ],
    include_package_data=True,
    version=UTMDriver.__version__,
    packages=find_packages(),
    url='https://github.com/maxpoint2point/UTMDriver',
    license='Apache-2.0 License',
    author='Максим',
    author_email='maxpoint2point@gmail.com',
    description='UTMDriver for EGAIS'
)
