# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtualbox_helper']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'remotevbox>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['main = virtualbox_helper.__main__:main',
                     'test = pytest:console_main']}

setup_kwargs = {
    'name': 'virtualbox-helper',
    'version': '0.1.2',
    'description': 'Start and control a virtualbox machine',
    'long_description': '# Virtualbox helper\n\nThis library helps to automate UI tasks on a Virtualbox machine using OpenCV.\n\nIt\'s based on `remotevbox` to interact with the SOAP service and `OpenCV` to\nperform region detection.\n\n__Features__:\n* can start the `vboxwebsrv` SOAP server programmatically and shut it down\n* match a region of the screen with a given fragment\n* wait for a fragment and click on its center\n* store if required a representation of the area it matched\n* accepts images as NumPy ndarray, raw bytes of filesystem paths\n\n## Installation\n\n    python3 -m pip install virtualbox_helper\n\n\n## Example usage\n\n```Python 3\n\nfrom virtualbox_helper import (\n    ensure_server_running,\n    get_machine,\n    wait_for_fragment,\n    wait_click_on_fragment,\n)\n\n# this starts the server and stops it when the interpreter exits\n# or you can use the command vboxwebsrv manually\nensure_server_running()\n\nmachine = get_machine(\'vbox\', \'yourpassphrase\', \'Debian testing\')\nmachine.launch()\n\nno_match = detect_fragment(screenshot_data, \'some/random_image.png\')\nassert no_match is None\n\ndetection = detect_fragment(screenshot_data, \'valid_element.png\')\nassert detection is not None\n# similarity score\nassert detection[0] > 0.9\n# coordinates of the bounding box that was detected\nassert detection[1] == (19, 59)\nassert detection[2] == (172, 114)\n\n# raw bytes or a numpy (X, Y, 3) matrix can be used instead of a file path\nbutton_data = open(\'button.png\', \'rb\').read()\ntarget = wait_click_on_fragment(machine, button_data, timeout=60.0)\n# target has the same structure of match above\n\nwait_for_fragment(machine, \'some/element/to/wait_for.png\')\n\nwith open(\'screenshot.png\', \'wb\') as f:\n    screenshot_data = machine.take_screenshot_to_bytes()\n    f.write(screenshot_data)\n\n# this functionality is part of remotevbox\nmachine.send_character_string(\'hello world\')\nmachine.send_key_combination([\'<enter>\'])\n\nmachine.poweroff()\n```\n\n## When shoulkd I use this?\n\nHopefully never! If you have a proper API for what you want to automate,\ngo with that.\nTo automate UI operations look into `PyAutoGUI`, and `Selenium` or `Puppeteer`\nfor the web.\n\nHowever, if you can\'t do that, for example if you are writing tests for\nTempleOS or something weird, then this may be fine.\n\n\n## Tests\n\nThe tests are based on pytest, can be run using `poetry run test`.\nThey expect a machine called "Debian testing" running Debian 11.\nShould be trivial to adapt to some other image.\n',
    'author': 'Jacopo Farina',
    'author_email': 'jacopo1.farina@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacopofar/virtualbox-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
