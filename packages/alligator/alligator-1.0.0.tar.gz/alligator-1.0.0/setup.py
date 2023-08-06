# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alligator', 'alligator.backends']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alligator',
    'version': '1.0.0',
    'description': 'Simple offline task queues.',
    'long_description': 'Alligator\n=========\n\n.. image:: https://travis-ci.org/toastdriven/alligator.png?branch=master\n        :target: https://travis-ci.org/toastdriven/alligator\n\nSimple offline task queues. For Python.\n\n`"See you later, alligator."`\n\nLatest documentation at http://alligator.readthedocs.org/en/latest/.\n\n\nRequirements\n------------\n\n* Python 3.6+\n* (Optional) ``redis`` for the Redis backend\n* (Optional) ``boto3>=1.12.0`` for the SQS backend\n\n\nBasic Usage\n-----------\n\nThis example uses Django, but there\'s nothing Django-specific about Alligator.\n\nI repeat, You can use it with **any** Python code that would benefit from\nbackground processing.\n\n.. code:: python\n\n    from alligator import Gator\n\n    from django.contrib.auth.models import User\n    from django.shortcuts import send_email\n\n\n    # Make a Gator instance.\n    # Under most circumstances, you would configure this in one place &\n    # import that instance instead.\n    gator = Gator(\'redis://localhost:6379/0\')\n\n\n    # The task itself.\n    # Nothing special, just a plain *undecorated* function.\n    def follow_email(followee_username, follower_username):\n        followee = User.objects.get(username=followee_username)\n        follower = User.objects.get(username=follower_username)\n\n        subject = \'You got followed!\'\n        message = \'Hey {}, you just got followed by {}! Whoohoo!\'.format(\n            followee.username,\n            follower.username\n        )\n        send_email(subject, message, \'server@example.com\', [followee.email])\n\n\n    # An simple, previously expensive view.\n    @login_required\n    def follow(request, username):\n        # You\'d import the task function above.\n        if request.method == \'POST\':\n            # Schedule the task.\n            # Use args & kwargs as normal.\n            gator.task(follow_email, request.user.username, username)\n            return redirect(\'...\')\n\n\nRunning Tasks\n-------------\n\nRather than trying to do autodiscovery, fanout, etc., you control how your\nworkers are configured & what they consume.\n\nIf your needs are simple, run the included ``latergator.py`` worker:\n\n.. code:: bash\n\n    $ python latergator.py redis://localhost:6379/0\n\nIf you have more complex needs, you can create a new executable file\n(bin script, management command, whatever) & drop in the following code.\n\n.. code:: python\n\n    from alligator import Gator, Worker\n\n    # Bonus points if you import that one pre-configured ``Gator`` instead.\n    gator = Gator(\'redis://localhost:6379/0\')\n\n    # Consume & handle all tasks.\n    worker = Worker(gator)\n    worker.run_forever()\n\n\nLicense\n-------\n\nNew BSD\n\n\nRunning Tests\n-------------\n\nAlligator has 95%+ test coverage & aims to be passing/stable at all times.\n\nIf you\'d like to run the tests, clone the repo, then run::\n\n    $ virtualenv -p python3 env\n    $ . env/bin/activate\n    $ pip install -r requirements-tests.txt\n    $ python setup.py develop\n    $ pytest -s -v --cov=alligator --cov-report=html tests\n\nThe full test suite can be run via:\n\n    $ export ALLIGATOR_TESTS_INCLUDE_SQS=true\n    $ ./tests/run_all.sh\n\nThis requires all backends/queues to be running, as well as valid AWS\ncredentials if ``ALLIGATOR_TESTS_INCLUDE_SQS=true`` is set.\n\n\nWHY?!!1!\n--------\n\n* Because I have NIH-syndrome.\n* Or because I longed for something simple (~375 loc).\n* Or because I wanted something with tests (90%+ coverage) & docs.\n* Or because I wanted pluggable backends.\n* Or because testing some other queuing system was a pain.\n* Or because I\'m an idiot.\n\n\nRoadmap\n-------\n\nPost-`1.0.0`:\n\n    * Expand the supported backends\n        * Kafka?\n        * ActiveMQ support?\n        * RabbitMQ support?\n        * ???\n',
    'author': 'Daniel Lindsley',
    'author_email': 'daniel@toastdriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toastdriven/alligator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
