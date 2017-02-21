SELECT_QUERY = "SELECT {columns} FROM `{table}` WHERE {filter};"

SEARCH_RANGE = {
    'contact': ['first_name', 'last_name'],
    'address': ['street', 'city', 'postal'],
    'phone': ['number']
}


search_data = {
        'search_words': ['a'],
        'filter': [
            {'table': 'f1_table', 'column': 'f1_column', 'values':  ['c', 'd', 'g']},
            {'table': 'f2_table', 'column': 'f2_column', 'values':  ['e', 'f']},
        ]
    }

# filter results
results = []
for filter in search_data['filter']:
    wheres = []
    for value in filter['values']:
        wheres.append("{col} = {val}".format(col=filter['column'], val=value))
    where = " OR ".join(wheres)
    query = SELECT_QUERY.format(
        columns='contact_id',
        table=filter['table'],
        filter=where
    )
    results.append(query)

# search words results
for word in search_data['search_words']:
    for table_name, columns in SEARCH_RANGE.iteritems():
        wheres = []
        for column in columns:
            wheres.append("{col} LIKE %{val}%".format(col=column, val=word))
        where = " OR ".join(wheres)
        target = 'id' if table_name == 'contact' else 'contact_id'
        query = SELECT_QUERY.format(
            columns=target,
            table=table_name,
            filter=where
        )
        results.append(query)

for result in results:
    print result
