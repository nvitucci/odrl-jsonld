import json

import pytest

from jsonschema import validate
from rdflib import Graph, compare


def compare_graphs(g1, g2):
    return compare.isomorphic(g1, g2)


@pytest.fixture(scope='module')
def context():
    with open('context.jsonld') as context_file:
        return json.load(context_file)


@pytest.fixture(scope='module')
def schema():
    with open('ODRL21.json') as odrl_schema_file:
        return json.load(odrl_schema_file)


@pytest.mark.parametrize('name', [
    'agreement',
    'display_and_distribute',
    'inheritance_1',
    'inheritance_2',
    'offer',
    'offer_and_next_policy_1',
    'offer_and_next_policy_2',
    'permission_and_prohibition',
    'privacy',
    'request',
    'set',
    'social_network',
    'ticket'
])
def test_example(context, schema, name):
    with open('tests/json/%s.json' % name) as example_file:
        example = json.load(example_file)

    # If this passes, validate was successful (it did not raise any exception)
    assert validate(example, schema) is None

    g_jsonld = Graph()
    g_jsonld.parse(location='tests/json/%s.json' % name, format='json-ld', context=context)

    g_ttl = Graph()
    g_ttl.parse(location='tests/ttl/%s.ttl' % name, format='turtle')

    # Check that the two graphs are isomorphic
    assert compare_graphs(g_jsonld, g_ttl)


def test_example_multiple_assets(context, schema):
    """This test is different because the example uses an array of JSON-LD contexts rather than just one"""
    name = 'multiple_assets'

    with open('tests/json/%s.json' % name) as example_file:
        example = json.load(example_file)

    # If this passes, validate was successful (it did not raise any exception)
    assert validate(example, schema) is None

    contexts = [
        context,
        {
            'x:collection': {'@id': 'http://example.com/x#collection', '@type': '@id'}
        }
    ]

    g_jsonld = Graph()
    g_jsonld.parse(location='tests/json/%s.json' % name, format='json-ld', context=contexts)

    g_ttl = Graph()
    g_ttl.parse(location='tests/ttl/%s.ttl' % name, format='turtle')

    # Check that the two graphs are isomorphic
    assert compare_graphs(g_jsonld, g_ttl)
