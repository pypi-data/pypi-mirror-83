# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['multiplex']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0',
 'aiostream>=0.4.1,<0.5.0',
 'click>=7.1.2,<8.0.0',
 'easy-ansi>=0.3,<0.4',
 'pyte>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['mp = multiplex.main:main']}

setup_kwargs = {
    'name': 'multiplex',
    'version': '0.2.0',
    'description': 'View output of multiple processes, in parallel, in the console, with an interactive TUI',
    'long_description': '# multiplex\nView output of multiple processes, in parallel, in the console, with an interactive TUI\n\n## Examples\n\n### Parallel Execution Of Commands\n\n```shell script\nmp \\\n    \'./some-long-running-process.py --zone z1\' \\\n    \'./some-long-running-process.py --zone z2\' \\\n    \'./some-long-running-process.py --zone z3\'\n```\n\n![Par](http://multiplex-static-files.s3-website-us-east-1.amazonaws.com/o.par.gif)\n\nYou can achive the same effect using Python API like this:\n\n```python\nfrom multiplex import Multiplex\n\nmp = Multiplex()\nfor zone in [\'z1\', \'z2\', \'z3\']:\n    mp.add(f"./some-long-running-process.py --zone {zone}")\nmp.run()\n```\n\n### Dynamically Add Commands\n\n`my-script.sh`:\n```shell script\n#!/bin/bash -e\necho Hello There\n\nexport REPO=\'git@github.com:dankilman/multiplex.git\'\n\nmp \'git clone $REPO\'\nmp \'pyenv virtualenv 3.8.5 multiplex-demo && pyenv local multiplex-demo\'\ncd multiplex\nmp \'poetry install\'\nmp \'pytest tests\'\n\nmp @ Goodbye -b 0\n```\n\nAnd then running: \n```shell script\nmp ./my-script.sh -b 7\n```\n\n![Seq](http://multiplex-static-files.s3-website-us-east-1.amazonaws.com/o.seq.gif)\n\n### Python Controller\nAn output similar to the first example can be achieved from a single process using\nthe Python Controller API.\n\n```python\nimport random\nimport time\nimport threading\n\nfrom multiplex import Multiplex, Controller\n\nCSI = "\\033["\nRESET = CSI + "0m"\nRED = CSI + "31m"\nGREEN = CSI + "32m"\nBLUE = CSI + "34m"\nMAG = CSI + "35m"\nCYAN = CSI + "36m"\n\nmp = Multiplex()\n\ncontrollers = [Controller(f"zone z{i+1}", thread_safe=True) for i in range(3)]\n\nfor controller in controllers:\n    mp.add(controller)\n\ndef run(index, c):\n    c.write(\n        f"Starting long running process in zone {BLUE}z{index}{RESET}, "\n        f"that is not really long for demo purposes\\n"\n    )\n    count1 = count2 = 0\n    while True:\n        count1 += random.randint(0, 1000)\n        count2 += random.randint(0, 1000)\n        sleep = random.random() * 3\n        time.sleep(sleep)\n        c.write(\n            f"Processed {RED}{count1}{RESET} orders, "\n            f"total amount: {GREEN}${count2}{RESET}, "\n            f"Time it took to process this batch: {MAG}{sleep:0.2f}s{RESET}, "\n            f"Some more random data: {CYAN}{random.randint(500, 600)}{RESET}\\n"\n        )\n\nfor index, controller in enumerate(controllers):\n    thread = threading.Thread(target=run, args=(index+1, controller))\n    thread.daemon = True\n    thread.start()\n\nmp.run()\n```\n\n![Cont](http://multiplex-static-files.s3-website-us-east-1.amazonaws.com/o.cont.gif)\n\n### Help Screen\nType `?` to toggle the help screen.\n\n![help](http://multiplex-static-files.s3-website-us-east-1.amazonaws.com/help.png)\n',
    'author': 'Dan Kilman',
    'author_email': 'dankilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dankilman/multiplex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
