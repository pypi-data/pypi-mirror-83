from delphai_utils.logging import logging
from delphai_utils.config import get_config
from elasticsearch import AsyncElasticsearch
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
es_host = get_config('elasticsearch.host')
es_index = get_config('elasticsearch.index')
es = AsyncElasticsearch(hosts=[f'http://{es_host}:80'])