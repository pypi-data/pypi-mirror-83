# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffsync']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0', 'structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'diffsync',
    'version': '1.0.0',
    'description': 'Library to easily sync/diff/update 2 different data sources',
    'long_description': '# DiffSync\n\nDiffSync is a utility library that can be used to compare and synchronize different datasets.\n\nFor example, it can be used to compare a list of devices from 2 inventories system and, if required, synchronize them in either direction.\n\n```python\nA = DiffSyncSystemA()\nB = DiffSyncSystemB()\n\nA.load()\nB.load()\n\n# it will show the difference between both systems\ndiff_a_b = A.diff_from(B)\nprint(diff.str())\n\n# it will update System A to align with the current status of system B\nA.sync_from(B)\n\n# it will update System B to align with the current status of system A\nA.sync_to(B)\n```\n\n# Getting Started\n\nTo be able to properly compare different datasets, DiffSync relies on a shared datamodel that both systems must use.\n\n## Define your model with DiffSyncModel\n\nDiffSyncModel is based on [Pydantic](https://pydantic-docs.helpmanual.io/) and is using Python Typing to define the format of each attribute.\nEach DiffSyncModel class supports the following class-level attributes:\n- `_modelname` (str) Define the type of the model, it\'s used to store the data internally (Mandatory)\n- `_identifiers` List(str) List of instance field names used as primary keys for this object (Mandatory)\n- `_shortname` List(str) List of instance field names to use for a shorter name (Optional)\n- `_attributes` List(str) List of additional instance field names for this object (Optional)\n- `_children` Dict: Dict of {`<modelname>`: `field_name`} to indicate how child objects should be stored. (Optional)\n\n> DiffSyncModel instances must be uniquely identified by their unique id, composed of all fields defined in `_identifiers`. DiffSyncModel does not support incremental IDs as primary key.\n\n```python\nfrom diffsync import DiffSyncModel\n\nclass Site(DiffSyncModel):\n    _modelname = "site"\n    _identifiers = ("name",)\n    _shortname = ()\n    _attributes = ("contact_phone",)\n    _children = {"device": "devices"}\n\n    name: str\n    contact_phone: str\n    devices: List = list()\n```\n\n### Relationship between models.\nCurrently the relationships between models are very loose by design. Instead of storing an object, it\'s recommended to store the uid of an object and retrieve it from the store as needed.\n\n## DiffSync\n\nA DiffSync object must reference each model available at the top of the object by its modelname and must have a `top_level` attribute defined to indicate how the diff and the synchronization should be done. In the example below, `"site"` is the only top level objects so the synchronization engine will check all sites and all children of each site (devices)\n\n```python\nfrom diffsync import DiffSync\n\nclass BackendA(DiffSync):\n\n    site = Site\n    device = Device\n\n    top_level = ["site"]\n```\n\nIt\'s up to the user to populate the internal cache with the appropriate data. In the example below we are using the `load()` method to populate the cache but it\'s not mandatory, it could be done differently\n\n## Store data in a DiffSync object\n\nTo add a site to the local cache/store, you need to pass a valid DiffSyncModel object to the `add()` function.\n```python\n\nclass BackendA(DiffSync):\n    [...]\n\n    def load(self):\n        # Store an individual object\n        site = self.site(name="nyc")\n        self.add(site)\n\n        # Store an object and define it as a children for another object\n        device = self.device(name="rtr-nyc", role="router", site_name="nyc")\n        self.add(device)\n        site.add_child(device)\n```\n\n## Update Remote system on Sync\n\nTo update a remote system, you need to extend your DiffSyncModel class(es) to define your own `create`, `update` and/or `delete` methods for each model.\nA DiffSyncModel instance stores a reference to its parent DiffSync class in case you need to use it to look up other model instances from the DiffSync\'s cache.\n\n```python\nclass Device(DiffSyncModel):\n    [...]\n\n    @classmethod\n    def create(cls, diffsync, ids, attrs):\n        ## TODO add your own logic here to create the device on the remote system\n        return super().create(ids=ids, diffsync=diffsync, attrs=attrs)\n\n    def update(self, attrs):\n        ## TODO add your own logic here to update the device on the remote system\n        return super().update(attrs)\n\n    def delete(self):\n        ## TODO add your own logic here to delete the device on the remote system\n        super().delete()\n        return self\n```\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
