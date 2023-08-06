# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctkinter']

package_data = \
{'': ['*']}

install_requires = \
['asyncgui>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'asynctkinter',
    'version': '0.1.1',
    'description': "async library that works on top of tkinter's event loop",
    'long_description': '# AsyncTkinter\n\nAsync library that works on top of tkinter\'s event loop.\n([Youtube](https://youtu.be/8XP1KgRd3jI))\n\n### Installation\n\n```\npip install asynctkinter\n```\n\n## Usage\n\n```python\nfrom tkinter import Tk, Label\nimport asynctkinter as at\nat.patch_unbind()\n\ndef heavy_task():\n    import time\n    for i in range(5):\n        time.sleep(1)\n        print(\'heavy task:\', i)\n\nroot = Tk()\nlabel = Label(root, text=\'Hello\', font=(\'\', 60))\nlabel.pack()\n\nasync def some_task(label):\n    label[\'text\'] = \'start heavy task\'\n\n    # wait until a label is pressed\n    event = await at.event(label, \'<Button>\')\n\n    print(event.x, event.y)\n    label[\'text\'] = \'running...\'\n\n    # create a new thread, run a function on it, then\n    # wait for the completion of that thread\n    result = await at.run_in_thread(heavy_task, after=label.after)\n    print(\'result of heavytask():\', result)\n\n    label[\'text\'] = \'done\'\n\n    # wait for 2sec\n    await at.sleep(2000, after=label.after)\n\n    label[\'text\'] = \'close the window\'\n\n\nat.start(some_task(label))\nroot.mainloop()\n```\n\n#### wait for the completion/cancellation of multiple tasks simultaneously\n\n```python\nasync def some_task(label):\n    from functools import partial\n    import asynctkinter as at\n    sleep = partial(at.sleep, after=label.after)\n    # wait until EITEHR a label is pressed OR 5sec passes\n    tasks = await at.or_(\n        at.event(label, \'<Button>\'),\n        sleep(5000),\n    )\n    print("The label was pressed" if tasks[0].done else "5sec passed")\n\n    # wait until BOTH a label is pressed AND 5sec passes"\n    tasks = await at.and_(\n        at.event(label, \'<Button>\'),\n        sleep(5000),\n    )\n```\n\n#### synchronization primitive\n\nThere is a Trio\'s [Event](https://trio.readthedocs.io/en/stable/reference-core.html#trio.Event) equivalent.\n\n```python\nimport asynctkinter as at\n\nasync def task_A(e):\n    print(\'A1\')\n    await e.wait()\n    print(\'A2\')\nasync def task_B(e):\n    print(\'B1\')\n    await e.wait()\n    print(\'B2\')\n\ne = at.Event()\nak.start(task_A(e))\n# A1\nak.start(task_B(e))\n# B1\ne.set()\n# A2\n# B2\n```\n\n## Note\n\n- Why is `patch_unbind()` necessary? Take a look at [this](https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding).\n',
    'author': 'Nattōsai Mitō',
    'author_email': 'flow4re2c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gottadiveintopython/asynctkinter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
