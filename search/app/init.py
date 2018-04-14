import os

elasticsearch_url = os.environ.get(
	'ELASTICSEARCH_URL',
	'http://localhost:9200/',
)
