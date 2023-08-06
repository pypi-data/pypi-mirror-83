# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aircloak_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.4,<2.0.0', 'psycopg2>=2.8.5,<3.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'aircloak-tools',
    'version': '0.2.0',
    'description': 'Tools for querying an Aircloak service.',
    'long_description': '[![GitHub license](https://img.shields.io/github/license/diffix/aircloak-tools)](https://github.com/diffix/aircloak-tools/blob/master/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/diffix/aircloak-tools)](https://github.com/diffix/aircloak-tools/issues)\n\n# Python Aircloak Tools\n\nTools for querying an Aircloak api. \n\nThis package contains two main components:\n- [Aircloak Api](#aircloak-api): Wrapper around psycopg to query Aircloak directly.\n- [Explorer](#explorer): An interface to Diffix Explorer for data analytics.\n\n## Aircloak Api\n\nThe main aim is to provide an Aircloak-friendly wrapper around `psycopg2`, and in particular to\nprovide clear error messages when something doesn\'t go as planned. \n\nQuery results are returned as `pandas` dataframes. \n\n## Explorer\n\nUses [Diffix Explorer](https://github.com/diffix/explorer) to return enhanced statistics. Please see the project homepage for further information about Explorer. \n\n## Installation\n\nThe package can be installed in youir local environment using pip:\n```\npip install aircloak-tools\n```\n\nTo use Explorer Features you will also need to run [Diffix Explorer](https://github.com/diffix/explorer).\n\n## Example\n\nThe following code shows how to initiate a connection and execute a query.\n\nAs a pre-requisite you should have a username and password for the postgres interface of an\nAircloak installation (ask your admin for these). Assign these values to `AIRCLOAK_PG_USER`\nand `AIRCLOAK_PG_PASSWORD` environment variables. \n\n\n```python\nimport aircloak_tools as ac\n\nAIRCLOAK_PG_HOST = "covid-db.aircloak.com"\nAIRCLOAK_PG_PORT = 9432\n\nAIRCLOAK_PG_USER = environ.get("AIRCLOAK_PG_USER")\nAIRCLOAK_PG_PASSWORD = environ.get("AIRCLOAK_PG_PASSWORD")\n\nTEST_DATASET = "cov_clear"\n\nwith ac.connect(host=AIRCLOAK_PG_HOST, port=AIRCLOAK_PG_PORT,\n                user=AIRCLOAK_PG_USER, password=AIRCLOAK_PG_PASSWORD, dataset=TEST_DATASET) as conn:\n\n    assert(conn.is_connected())\n\n    tables = conn.get_tables()\n\n    print(tables)\n\n    feeling_now_counts = conn.query(\'\'\'\n    select feeling_now, count(*), count_noise(*)\n    from survey\n    group by 1\n    order by 1 desc\n    \'\'\')\n```\n\nThe easiest way to use Diffix Explorer is with the Docker image on [docker hub](https://docker.pkg.github.com/diffix/explorer/explorer-api). More detailed information on running Diffix Explorer is available at the [project repo](https://github.com/diffix/explorer). As an example, you can use explorer to generate sample data based on the anonymized dataset as follows:\n\n```python\nfrom aircloak_tools import explorer\n\nEXPLORER_URL = "http://localhost"\nEXPLORER_PORT = 5000\nDATASET = "gda_banking"\nTABLE = "loans"\nCOLUMNS = ["amount", "duration"]\n\nsession = explorer.explorer_session(base_url=EXPLORER_URL, port=EXPLORER_PORT)\nresult = explorer.explore(session, DATASET, TABLE, COLUMNS)\n\nassert result[\'status\'] == \'Complete\'\n\nprint(f\'{COLUMNS[0] : >10} |{COLUMNS[1] : >10}\')\nfor row in result[\'sampleData\']:\n    print(f\'{row[0] : >10} |{row[1] : >10}\')\n\n# Should print something like:\n#\n#    amount |  duration\n#     33000 |        12\n#     43000 |        36\n#     57000 |        12\n#     91000 |        24\n#     97000 |        48\n#    101000 |        60\n#\n# etc.\n```\n',
    'author': 'dlennon',
    'author_email': '3168260+dandanlen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diffix/aircloak-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
