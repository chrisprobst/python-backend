# coding=utf-8

"""

TODOS:
- add simple db operations
- add JSON compatible interfaces
- refactor ContractController

insert:
insert_into_table(table, data)


DATABASE INFORMATION AS JSON:
data = {
    table1: {
        column1: value1,
        column2: value2,
        ...
    },
    table2: {
        column1: value1,
        column2: value2,
        ...
    },
    ...
}

VOCABULARY

DATABASE ROW or ROW or ROW DATASET:
----------------------------------
row = {
    column: value,
    column: value,
    ...
}

"""


class BaseController(object):
    
    QUERY_INSERT = u"INSERT INTO {table} {columns} VALUES ({placeholders});"
    QUERY_SELECT = u"SELECT * FROM {table} WHERE {column}=?;"
    QUERY_SELECT_COLUMNS_BY_SINGLE_VALUE = u"SELECT {columns} FROM {table} WHERE {key}=?;"
    QUERY_GET_TABLE_INFO = u"PRAGMA table_info({table});"
    QUERY_SELECT_FROM_TABLE = u"SELECT * FROM {table};"
    QUERY_SELECT_COLUMNS = u"SELECT {columns} FROM {table};"
    
    MSG_ERROR_INSERT = u"Insert query \"{query}\" with values ({values}) returned error: {error}"
    MSG_ERROR_SELECT = u"Select query \"{query}\" with values ({values}) returned error: {error}"
    MSG_ERROR_VERIFY_COLUMNS = u"Could not verify column {col} in table {table}"
    
    MSG_DEBUG_SELECT = u"Select query \"{query}\" with values {values} did not return any rows"
    
    @staticmethod
    def create_placeholders_for_columns(columns):
        """
        Given a collection of columns [c_1, ..., c_n] this methods returns a
        string of sqlite3 placeholders "?, ..., ?" to insert into a query
        
        :param columns: (iterable) A collection of column names
        :return: (str) Placeholders to insert into a query
        """
        return u",".join(u"?"*len(columns))
    
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
                self.insert_row_in_table(table_name, row, commit=False)
        self.database.commit()
    
    def insert_row_in_table(self, table_name, row, commit=True):
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
        :return: The generated id for the inserted row
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
            raise e
        if commit:
            self.database.commit()
        return self.database.cursor.lastrowid
    
    def insert_rows_in_table(self, table, rows, commit=True):
        for row in rows:
            self.insert_row_in_table(table, row, commit=commit)
    
    def select_rows(self, table):
        """
        Selects all existing rows from a given table.

        :param table: (str) The table to select from
        :return: ([tuple]) A list of all existing rows
        """
        query = BaseController.QUERY_SELECT_FROM_TABLE.format(table=table)
        self.database.cursor.execute(query)
        results = self.database.cursor.fetchall()
        return results
    
    def select_columns(self, table, columns):
        self.verify_columns_for_table(table, columns)
        arg_columns = u", ".join(columns)
        query = BaseController.QUERY_SELECT_COLUMNS.format(
            columns=arg_columns,
            table=table
        )
        self.database.cursor.execute(query)
        results = self.database.cursor.fetchall()
        return results
    
    def select_rows_by_single_value(self, table, column, value):
        """
        This method selects all columns from a table with a simple
        equality filter for one filter column. The function call will
        produce and execute a query in the form:
        
        SELECT * FROM <query> WHERE <column>=<value>;
        
        :param table: (str) Table name
        :param column: (str) Name of the filter column
        :param value:
        :return:
        """
        query = BaseController.QUERY_SELECT.format(
            table=table,
            column=column
        )
        try:
            self.database.cursor.execute(query, (value,))
            results = self.database.cursor.fetchall()
            if len(results) == 0:
                self.database.logger.debug(BaseController.MSG_DEBUG_SELECT.format(
                    query=query,
                    values=value
                ))
            return results
        except BaseException, e:
            self.database.logger.error(BaseController.MSG_ERROR_SELECT.format(
                query=query,
                values=value,
                error=repr(e)
            ))
            raise e
    
    def get_table_info(self, table):
        query = BaseController.QUERY_GET_TABLE_INFO.format(table=table)
        self.database.cursor.execute(query)
        result = self.database.cursor.fetchall()
        named_result = []
        for table_info in result:
            # TODO: figure out the remaining data fields!
            named_result.append(
                {
                    u"id": table_info[0],
                    u"column_name": table_info[1],
                    u"column_type": table_info[2],
                    u"unknown data_1": table_info[3],
                    u"unknown data_2": table_info[4],
                    u"unknown data_3": table_info[5]
                }
            )
        return named_result
    
    def get_columns_for_table(self, table):
        table_info = self.get_table_info(table)
        return [e[u"column_name"] for e in table_info]
    
    def verify_columns_for_table(self, table, columns):
        if columns == ("*",):
            return
        valid_columns = self.get_columns_for_table(table)
        for column in columns:
            if column not in valid_columns:
                raise ValueError(BaseController.MSG_ERROR_VERIFY_COLUMNS.format(
                    col=column,
                    table=table
                ))
    
    def select_columns_by_single_value(self, table, columns, key, value):
        self.verify_columns_for_table(table, columns)
        arg_columns = u", ".join(columns)
        query = BaseController.QUERY_SELECT_COLUMNS_BY_SINGLE_VALUE.format(
            columns=arg_columns,
            table=table,
            key=key
        )
        try:
            self.database.cursor.execute(query, (value,))
            results = self.database.cursor.fetchall()
            if len(results) == 0:
                self.database.logger.debug(BaseController.MSG_DEBUG_SELECT.format(
                    query=query,
                    values=value
                ))
            return results
        except BaseException, e:
            self.database.logger.error(BaseController.MSG_ERROR_SELECT.format(
                query=query,
                values=value,
                error=repr(e)
            ))
            raise e
        


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
    try:
        ctr.insert_into_database(data)
    except:
        print "fehler"
    results = ctr.select_rows_by_single_value("phone", "contact_id", 10)
    print results[0][0]
    print results[0]["id"]
    print ctr.get_columns_for_table("users")
