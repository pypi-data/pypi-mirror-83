[![GitHub license](https://img.shields.io/github/license/diffix/aircloak-tools)](https://github.com/diffix/aircloak-tools/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/diffix/aircloak-tools)](https://github.com/diffix/aircloak-tools/issues)

# Python Aircloak Tools

Tools for querying an Aircloak api. 

This package contains two main components:
- [Aircloak Api](#aircloak-api): Wrapper around psycopg to query Aircloak directly.
- [Explorer](#explorer): An interface to Diffix Explorer for data analytics.

## Aircloak Api

The main aim is to provide an Aircloak-friendly wrapper around `psycopg2`, and in particular to
provide clear error messages when something doesn't go as planned. 

Query results are returned as `pandas` dataframes. 

## Explorer

Uses [Diffix Explorer](https://github.com/diffix/explorer) to return enhanced statistics. Please see the project homepage for further information about Explorer. 

## Installation

The package can be installed in youir local environment using pip:
```
pip install aircloak-tools
```

To use Explorer Features you will also need to run [Diffix Explorer](https://github.com/diffix/explorer).

## Example

The following code shows how to initiate a connection and execute a query.

As a pre-requisite you should have a username and password for the postgres interface of an
Aircloak installation (ask your admin for these). Assign these values to `AIRCLOAK_PG_USER`
and `AIRCLOAK_PG_PASSWORD` environment variables. 


```python
import aircloak_tools as ac

AIRCLOAK_PG_HOST = "covid-db.aircloak.com"
AIRCLOAK_PG_PORT = 9432

AIRCLOAK_PG_USER = environ.get("AIRCLOAK_PG_USER")
AIRCLOAK_PG_PASSWORD = environ.get("AIRCLOAK_PG_PASSWORD")

TEST_DATASET = "cov_clear"

with ac.connect(host=AIRCLOAK_PG_HOST, port=AIRCLOAK_PG_PORT,
                user=AIRCLOAK_PG_USER, password=AIRCLOAK_PG_PASSWORD, dataset=TEST_DATASET) as conn:

    assert(conn.is_connected())

    tables = conn.get_tables()

    print(tables)

    feeling_now_counts = conn.query('''
    select feeling_now, count(*), count_noise(*)
    from survey
    group by 1
    order by 1 desc
    ''')
```

The easiest way to use Diffix Explorer is with the Docker image on [docker hub](https://docker.pkg.github.com/diffix/explorer/explorer-api). More detailed information on running Diffix Explorer is available at the [project repo](https://github.com/diffix/explorer). As an example, you can use explorer to generate sample data based on the anonymized dataset as follows:

```python
from aircloak_tools import explorer

EXPLORER_URL = "http://localhost"
EXPLORER_PORT = 5000
DATASET = "gda_banking"
TABLE = "loans"
COLUMNS = ["amount", "duration"]

session = explorer.explorer_session(base_url=EXPLORER_URL, port=EXPLORER_PORT)
result = explorer.explore(session, DATASET, TABLE, COLUMNS)

assert result['status'] == 'Complete'

print(f'{COLUMNS[0] : >10} |{COLUMNS[1] : >10}')
for row in result['sampleData']:
    print(f'{row[0] : >10} |{row[1] : >10}')

# Should print something like:
#
#    amount |  duration
#     33000 |        12
#     43000 |        36
#     57000 |        12
#     91000 |        24
#     97000 |        48
#    101000 |        60
#
# etc.
```
