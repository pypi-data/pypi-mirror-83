# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sla_calculator']

package_data = \
{'': ['*']}

install_requires = \
['holidays==0.10.3', 'pendulum==2.1.2']

setup_kwargs = {
    'name': 'sla-calculator',
    'version': '1.0.0',
    'description': 'A python module that will calculate the sla time based on working hours and holidays.',
    'long_description': '# SLA Calculator\n\n## Installation\n```\npip install sla-calculator\n```\n## Usage\nTo use this calculator, you must provide a starting time, the open time \nfor business, the closing time for business, the country whose holidays\nyou observe, and the sla time in hours.  The function will then take\ninto account all holidays and weekends as none working hours, and return \na pendulum object of the time the sla needs to be met by. The following\nexample will provide you with an SLA time 4 working hours from\n12/10/2019 1:02:03 UTC\n```python\nfrom sla_calculator import SLA_Calculator\n\nsla_calc = SLA_Calculator()\n\nsla_time = sla_calc.calculate(start_time="2019-12-10T01:02:03Z",\n                              open_hour=9,\n                              close_hour=17,\n                              country_name="US",\n                              sla_in_hours=4)\nprint(sla_time.to_iso8601_string())\n```\n\n## Locale Specification\nYou can also specify the province or state that you are in to get a more\nspecific set of holidays:\n```python\nsla_time = sla_calc.calculate(start_time="2019-12-10T01:02:03Z",\n                              open_hour=9,\n                              close_hour=17,\n                              country_name="US",\n                              sla_in_hours=4,\n                              state="CO")\n```\nOr:\n```python\nsla_time = sla_calc.calculate(start_time="2019-12-10T01:02:03Z",\n                              open_hour=9,\n                              close_hour=17,\n                              country_name="Switzerland",\n                              sla_in_hours=4,\n                              province="Zurich")\n```\n\n## Run tests\nTest are written for the pytest framework. Install it with:\n\n    $ poetry install pytest\n    \nRun the tests with:\n\n    $ poetry run pytest\n',
    'author': 'Michael Butler',
    'author_email': 'michael.butler@swimlane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/swimlane/sla_calculator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
