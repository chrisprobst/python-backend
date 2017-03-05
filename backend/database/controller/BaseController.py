# coding=utf-8

class BaseController(object):
    
    QUERY_INSERT = "INSERT INTO {table} {columns} VALUES ({placeholders})"
    
    MSG_ERROR_INSERT = "Insert query \"{query}\" with values ({values}) returned error: {error}"
    
    @staticmethod
    def create_placeholders_for_columns(columns):
        """
        Given a collection of columns [c_1, ..., c_n] this methods returns a
        string of sqlite3 placeholders "?, ..., ?" to insert into a query
        
        :param columns: (iterable) A collection of column names
        :return: (str) Placeholders to insert into a query
        """
        return ",".join("?"*len(columns))
    
    @staticmethod
    def extract_table_data(data):
        """
        Given a row dataset
        
        {
            column1: value1,
            column2: value2,
            ...
        }
        
        This method extrcts and returns the columns as a list, the values as a list
        and a pre-computed string of placeholders to insert into a query.
        
        :param data: (dict) A table dataset
        :return: (tuple) (columns, values, placeholders)
        """
        columns = tuple(data.keys())
        values = tuple(data.values())
        placeholders = BaseController.create_placeholders_for_columns(columns)
        return columns, values, placeholders
    
    def __init__(self, database):
        self.database = database
    
    def insert_into_database(self, data):
        """
        This method will insert any number of rows into any number of tables.
        Given a dictionary
        
        {
            table1_name: [row1, row2, row3, ...],
            table2_name: [row1, row2, ...],
            ...
        }
        
        this method will insert each to each table sequentially.
        
        NOTE:
        - Changes will only be commited, if every insertion was successful.
        - Changes will be aborted otherwise.
        - If changes are aborted, this method will re-raise the original exception
        
        
        :param data: (dict) Data to insert
        :return: (None)
        """
        for table_name, rows_to_insert in data.iteritems():
            for row in rows_to_insert:
                self.insert_single_row_in_table(table_name, row, commit=False)
        self.database.commit()
    
    def insert_single_row_in_table(self, table_name, row, commit=True):
        """
        Given a table name and a row dataset
        
        {
            column1: value1,
            column2: value2,
            ...
        }
        
        this method will insert the row into the table.
        
        NOTE:
        - Changes will be aborted if the insertion was not successful.
        - If changes are aborted, this method will re-raise the original exception.
        
        :param table_name: (str) Table name
        :param row: (dict) The row dataset (see above)
        :param commit: (bool) If True, changes will be commited after calling this method.
        :return:
        """
        columns, values, placeholders = BaseController.extract_table_data(row)
        query = BaseController.QUERY_INSERT.format(
            table=table_name,
            columns=columns,
            placeholders=placeholders
        )
        try:
            self.database.cursor.execute(query, values)
        except BaseException, e:
            self.database.rollback()
            self.database.logger.error(BaseController.MSG_ERROR_INSERT.format(
                query=query,
                values=values,
                error=repr(e)
            ))
        if commit:
            self.database.commit()

# TODO: fix this shit!
# Simple test
if __name__ == "__main__":
    from backend.database.Database import Database
    import logging
    logging.basicConfig()
    dbs = Database("../../../myDatabase.db", logging.getLogger())
    data = {
        "phone": [
            {
                "id": 100,
                "contact_id": 10,
                "description": "Nummer 1",
                "number": "123456789"
            },
            {
                "id": 101,
                "contact_id": 10,
                "description": "Nummer 2",
                "number": "987654321"
            },
            {
                "id": 102,
                "contact_id": 11,
                "description": "Nummer 1",
                "number": "123456789000000000"
            }
        ]
    }
    ctr = BaseController(dbs)
    ctr.insert_into_database(data)





