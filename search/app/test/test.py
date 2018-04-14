from pandasticsearch import DataFrame
df = DataFrame.from_es(url='http://localhost:9200',index='article')

df.print_schema()
