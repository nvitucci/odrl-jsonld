# odrl-jsonld

A JSON-LD context for [ODRL](https://www.w3.org/community/odrl/json/2.1/).

# Testing

Python 2.7 should be installed in order to run the tests. Virtualenv is also recommended.

## How to test

From the command line:

```sh
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
py.test
```

Each test checks whether the corresponding example:

* is valid with respect to the JSON schema;
* is equivalent to its Turtle version.

