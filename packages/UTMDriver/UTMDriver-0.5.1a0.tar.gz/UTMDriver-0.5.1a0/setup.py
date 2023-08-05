from setuptools import setup, find_packages
import UTMDriver

setup(
    data_files=[
        ('xml', [
            'UTMDriver/generic/queries/documents/templates/ActWriteOfShop_v2.xml',
            'UTMDriver/generic/queries/documents/templates/QueryNATTN.xml',
            'UTMDriver/generic/queries/documents/templates/QueryResendDoc.xml',
            'UTMDriver/generic/queries/documents/templates/QueryRests.xml',
            'UTMDriver/generic/queries/documents/templates/QueryRestsShop_v2.xml',
            'UTMDriver/generic/queries/documents/templates/TransferToShop.xml',
            'UTMDriver/generic/queries/documents/templates/WayBillAct_v3.xml',
            'UTMDriver/generic/queries/documents/templates/WriteOfShop_v2.xml',
            ]
         )
    ],
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
    version=UTMDriver.__version__,
    packages=find_packages(),
    url='https://github.com/maxpoint2point/UTMDriver',
    license='Apache-2.0 License',
    author='Максим',
    author_email='maxpoint2point@gmail.com',
    description='UTMDriver for EGAIS'
)
