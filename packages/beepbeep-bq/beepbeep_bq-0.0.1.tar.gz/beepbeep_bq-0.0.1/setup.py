import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="beepbeep_bq",
  packages=["beepbeep_bq"],
  version="0.0.1",
  description="",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Jim Barlow",
  author_email="jim@beepbeep.technology",
  license='Apache License 2.0',
  #download_url='https://github.com/',
  zip_safe=False,
  install_requires=
  [
    'cachetools==4.1.1',
    'certifi==2020.6.20',
    'chardet==3.0.4',
    'google-api-core==1.23.0',
    'google-auth==1.22.1',
    'google-cloud-bigquery==2.2.0',
    'google-cloud-core==1.4.3',
    'google-crc32c==1.0.0',
    'google-resumable-media==1.1.0',
    'googleapis-common-protos==1.52.0',
    'grpcio==1.33.1',
    'idna==2.10',
    'proto-plus==1.11.0',
    'protobuf==3.13.0',
    'pyasn1==0.4.8',
    'pyasn1-modules==0.2.8',
    'pytz==2020.1',
    'requests==2.24.0',
    'rsa==4.6',
    'six==1.15.0',
    'urllib3==1.25.11'
  ]
)
