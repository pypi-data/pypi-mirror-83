# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygame_colliders']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'pygame-colliders',
    'version': '0.1.4',
    'description': 'Polygon collider library for Pygame',
    'long_description': 'Pygame Colliders\n================\n\nPygame colliders will enhance your game or application to have more complex\ncolliding system beyond standard ``Rect`` colliders in Pygame.\n\nDespite the name colliders aren\'t bound to Pygame and Pygame library is not\nprerequisite.\n\nDocumentation\n-------------\n\nDocumentation is located at https://pygame-colliders.readthedocs.io/\n\nUsage\n-----\n\nLook how easy it is to use:\n\n.. code-block:: python\n\n    from pygame_colliders import ConcaveCollider, ConvexCollider\n\n    # Create colliders\n    collider_a_points = [(3, 3), (5, 3), (5, 4), (4, 4), (4, 5), (5, 5), (5, 6), (3, 6)]\n    collider_b_points = [(4.5, 3.5), (6, 2), (6, 4)]\n\n    collider_a = ConcaveCollider(poly_a_points)\n    collider_b = ConvexCollider(poly_b_points)\n\n    # Check collision\n    if collider_a.collide(collider_b):\n        print("Collision detected!")\n\nFeatures\n--------\n\nCollisions between\n\nInstallation\n------------\n\nInstall pygame colliders by running:\n\n    pip install pygame-colliders\n\nContribute\n----------\n\n- Issue Tracker: https://github.com/jtiai/pygame-colliders/issues\n- Source Code: https://github.com/jtiai/pygame-colliders\n\nSupport\n-------\n\nIf you are having issues, please let us know.\nWe have a Discord channel located at : https://discord.gg/VXVRPxe\n\nLicense\n-------\n\nThe project is licensed under the 3-clause BSD license.\n',
    'author': 'Jani Tiainen',
    'author_email': 'jani@tiainen.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtiai/pygame-colliders',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
