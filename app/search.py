from flask import current_app
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    try:
        current_app.elasticsearch.index(index=index, id=model.id, body=payload)
    except (ConnectionError, ConnectionTimeout):
        print("Error: Record not added! Could not connect to Elasticsearch service")


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    try:
        current_app.elasticsearch.delete(index=index, id=model.id)
    except (ConnectionError, ConnectionTimeout):
        print("Error: Record not deleted! Could not connect to Elasticsearch service")


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    try:
        search = current_app.elasticsearch.search(
            index=index,
            body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                'from': (page - 1) * per_page, 'size': per_page})
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids, search['hits']['total']['value']
    except (ConnectionError, ConnectionTimeout):
        print("Error: Search failed. Could not connect to Elasticsearch service")
        return [], 0
