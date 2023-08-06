import os
import shutil
from setuptools import find_packages, setup
rootdir = os.path.abspath(os.path.dirname(__file__))
os.makedirs('/opt/netbox/docs/models/netbox_work_logs', exist_ok=True)
shutil.copy2(rootdir + '/netbox_work_logs/doc/vmworklog.md', 
             '/opt/netbox/docs/models/netbox_work_logs')
shutil.copy2(rootdir + '/netbox_work_logs/doc/deviceworklog.md',
             '/opt/netbox/docs/models/netbox_work_logs')

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='netbox-work-logs',
    version='1.2.1',
    description='A NetBox work logs plugin',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vas-git/netbox-work-logs',
    author='Vasilatos Vitaliy',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
