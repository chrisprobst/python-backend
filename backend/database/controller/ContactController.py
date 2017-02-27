#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import itertools


class ContactController(object):
    
    # TODO: Remove 'json' parameters since they are implicit and unuseful
    
    # TODO: Export to BaseController
    TABLE_COLUMNS = {
        "contact": ["id", "prefix", "first_name", "last_name", "birth_date", "comment"],
        "mail": ["contact_id", "description", "address"],
        "phone": ["contact_id", "description", "number"],
        "address": ["contact_id", "description", "street", "number", "addr_extra", "postal", "city"],
        "study": ["contact_id", "status", "school", "course", "start", "end", "focus", "degree"]
    }

    SEARCH_RANGE = {
        'contact': ['first_name', 'last_name'],
        'address': ['street', 'city', 'postal'],
        'phone': ['number']
    }


    # TODO: Export to BaseController
    SELECT_QUERY = "SELECT {columns} FROM `{table}` WHERE {filter};"
    SELECT_QUERY_NO_WHERE = "SELECT {columns} FROM `{table}`;"
    INSERT_QUERY = "INSERT INTO `{table}` ({columns}) VALUES ({placeholders});"
    UPDATE_QUERY = "UPDATE `{table}` SET {updates} WHERE {filter};"
    DELETE_QUERY = "DELETE FROM `{table}` WHERE {filter};"
    DELETE_BY_ID_QUERY = "DELETE FROM `{table}` WHERE {id}=?;"
    QUERY_SELECT_ALL_CONTACT_IDS = "SELECT id FROM `contact`;"
    
    SEARCH_QUERY_PARTIAL_1 = "{table}.{column} = ?"
    SEARCH_QUERY_PARTIAL_2 = "({partial_1})"
    SEARCH_QUERY_SEARCH_RANGE = "( x LIKE %a% AND y LIKE %b% AND ... )"
    
    filteres = """
    (
        (
            (table.col1=value) OR (table.col1=value) OR ...
        )
        AND
        (
            (table.col2=value) OR (table.col2=value) OR ...
        )
        ...
        AND
        (
            (table.col_n=value) OR ...
        )
    """
    
    search_range_statement = """
    (
        (col1 LIKE %word1% AND col1 LIKE %word2% AND ... AND col1 LIKE %word_n%)
        OR
        ...
    )
    """
    
    
    SEARCH_QUERY = """
        SELECT contact.id
        FROM contact
        LEFT JOIN address ON contact.id = address.contact_id
        LEFT JOIN phone ON contact.id = phone.contact_id
        LEFT JOIN study ON contact.id = study.contact_id
        INNER JOIN member ON contact.id = member.contact_id
        INNER JOIN ressort ON member.ressort = ressort.id
        WHERE
                {filters}
            AND
                {search_range_statements}
        ORDER BY
            contact.id;
    """
    
    DUMMY_CONTACT_DATA = {
        "contact": {
            "prefix": "Herr",
            "first_name": "Vorname",
            "last_name": "Nachname",
            "birth_date": "dd.mm.yyy",
            "comment": "Test-Kommentar"
        },
        "mail": [
            {"description": "Test Mail1", "address": "alex1@alex.de"}
        ],
        "address": [
            {"description": "Privat", "street": "Gilbachstrasse", "number": "7-9", "addr_extra": "", "postal": "40219", "city": "Duesseldorf"}
        ],
        "phone": [
            {"description": "Privat1", "number": "0123456789"}
        ],
        "study": [
            {"status": "done", "school": "HHU", "course": "Informatik", "start": "dd.mm.yyyy", "end": "dd.mm.yyyy", "focus": "Netzwerksicherheit", "degree": "b_a"}
        ]
    }

    @staticmethod
    def _columns_are_invalid_for_table(columns, table):
        valid_columns = ContactController.TABLE_COLUMNS[table]
        for col in columns:
            if col not in valid_columns:
                return True
        return False
    
    # TODO: Database will be passed to BaseController
    def __init__(self, database):
        self.database = database
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                        CREATE METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # TODO: Check if commit field is in every method
    def create_contact(self, contact, commit=True):
        """
        Creates a new contact in the database given a contact structure. Note: since this contact is
        new, no "id" field in the "contact" data is required, just as no "contact_id" fields are
        required in "mail", "phone", "address" oder "study".
        
        :param contact: (dict) A contact structure (no IDs required!)
        :param commit: (bool) If true, all changes will be committed at the end of the function call
        :return: (int) The generated contact id for the new contact record
        """
        try:
            contact_id = self._insert_json_in_table(contact["contact"], "contact")
            for mail in contact["mail"]:
                mail["contact_id"] = contact_id
                self._insert_json_in_table(mail, "mail")
            for address in contact["address"]:
                address["contact_id"] = contact_id
                self._insert_json_in_table(address, "address")
            for phone in contact["phone"]:
                phone["contact_id"] = contact_id
                self._insert_json_in_table(phone, "phone")
            for study in contact["study"]:
                study["contact_id"] = contact_id
                self._insert_json_in_table(study, "study")
            if commit:
                self.database.commit()
            return contact_id
        except BaseException, e:
            self.database.rollback()
            raise e
    
    def create_contacts(self, contacts):
        """
        Expects a list of contact structures and calls create_contact() on each of them.
        
        :param contacts: ([dict]) A list of contact structures
        :return: ([int]) A list of the respective contact ids
        """
        contact_ids = []
        try:
            for contact in contacts:
                new_contact_id = self.create_contact(contact, commit=False)
                contact_ids.append(new_contact_id)
            self.database.commit()
            return contact_ids
        except BaseException, e:
            self.database.rollback()
            raise e
    
    # TODO: Shouldn't stay for ever
    def create_dummy_contact(self):
        """
        Creates a dummy contact (a contact with fixed data).
        
        :return: (int) The generated contact id for the new contact record
        """
        self.create_contact(ContactController.DUMMY_CONTACT_DATA)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                        READ METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def select_contact_for_id(self, contact_id):
        """
        Select a contact structure from database for a given ID.

        :param contact_id: (int) The contact id to fetch from the database
        :return: (dict) The matching contact structure or an empty dictionary
        """
        id_filter = "id={id}".format(id=contact_id)
        contact_id_filter = "contact_id={id}".format(id=contact_id)
        result_contact = self._select_named_data(["*"], "contact", id_filter)
        result_mail = self._select_named_data(["*"], "mail", contact_id_filter)
        result_phone = self._select_named_data(["*"], "phone", contact_id_filter)
        result_address = self._select_named_data(["*"], "address", contact_id_filter)
        result_study = self._select_named_data(["*"], "study", contact_id_filter)
        if len(result_contact) != 1:
            return {}
        contact = {
            "contact": result_contact[0],
            "mail": result_mail,
            "phone": result_phone,
            "address": result_address,
            "study": result_study
        }
        return contact
    
    def select_contacts_for_ids(self, ids):
        """
        Select multiple contact structures for a given list of IDs.
        
        :param ids: ([int]) List of contact ids to fetch from the database
        :return: ([dict]) A list of matching contact structures (can contain empty dicts for not matching IDs)
        """
        contacts = []
        for contact_id in ids:
            contacts.append(self.select_contact_for_id(contact_id))
        return contacts
    
    def select_all_contact_ids(self):
        """
        Selects all existing contact IDs from the database.
        
        :return: ([int]) A list of all existing contact IDs
        """
        self.database.cursor.execute(ContactController.QUERY_SELECT_ALL_CONTACT_IDS)
        contact_ids = [result[0] for result in self.database.cursor.fetchall()]
        return contact_ids
    
    def select_all_contacts(self):
        """
        Calls select_contacts_for_ids with select_all_contact_ids() as argument.
        
        :return: ([dict])  A list of all contact structures
        """
        contact_ids = self.select_all_contact_ids()
        return self.select_contacts_for_ids(contact_ids)
    
    # TODO: NO HANDLER YET!
    def select_contact_ids_by_filter(self, contact_filter):
        """
        Finds all contact ids of contacts matching the given filter.
        NOTE: The filter structure is not completely done, so please do not use this method by now!
        
        :param contact_filter:
        :return: ([int]) A list of matching contact ids
        """
        # TODO: WARNING! This works but it doesnt work good
        # Find contact_ids that match their respective filter
        result_contact_ids = set(
            [d["id"] for d in self._select_named_data(
                ["id"],
                "contact",
                contact_filter["contact"]["filter"]
            )]
        )
        result_mail_contact_ids = set(
            [d["contact_id"] for d in self._select_named_data(
                ["contact_id"],
                "mail",
                contact_filter["mail"]["filter"]
            )]
        )
        result_phone_contact_ids = set(
            [d["contact_id"] for d in self._select_named_data(
                ["contact_id"],
                "phone",
                contact_filter["phone"]["filter"]
            )]
        )
        result_address_contact_ids = set(
            [d["contact_id"] for d in self._select_named_data(
                ["contact_id"],
                "address",
                contact_filter["address"]["filter"]
            )]
        )
        result_study_contact_ids = set(
            [d["contact_id"] for d in self._select_named_data(
                ["contact_id"],
                "study",
                contact_filter["study"]["filter"]
            )]
        )
        all_contact_ids = set(self.select_all_contact_ids())
        # Apply all filters
        if contact_filter["mail"]["filter"]:
            all_contact_ids = all_contact_ids.intersection(result_mail_contact_ids)
        if contact_filter["phone"]["filter"]:
            all_contact_ids = all_contact_ids.intersection(result_phone_contact_ids)
        if contact_filter["address"]["filter"]:
            all_contact_ids = all_contact_ids.intersection(result_address_contact_ids)
        if contact_filter["study"]["filter"]:
            all_contact_ids = all_contact_ids.intersection(result_study_contact_ids)
        if contact_filter["contact"]["filter"]:
            all_contact_ids = all_contact_ids.intersection(result_contact_ids)
        return list(all_contact_ids)
    
    # TODO: NO HANDLER YET!
    def select_contacts_by_search(self, search_data):
        # TODO: NOT IMPLEMENTED YET
        """
        post structure
            {
                searchs_words: [a, b]
                filter-f1_table-f1_column : [c, d],
                filter-f2_table-f2_column : [e, f]
            }
        ------
        search_data: {
            'search_words': [a, b, ...],
            'filter': [
                {'table': 'f1_table', 'column': 'f1_column', 'values':  [c, d, ...]},
                {'table': 'f2_table', 'column': 'f2_column', 'values':  [e, f, ...]},
                ...
            ]
        }
        """
        # TODO: prevent tables and columns from SQL injection
        # filter results
        results = []
        for filter in search_data['filter']:
            wheres = []
            values = filter["values"]
            for i in range(len(filter['values'])):
                wheres.append("{table}.{column} = ?".format(table=filter['table'], column=filter['column']))
            where = " OR ".join(wheres)
            table_name = filter['table']
            target = 'id' if table_name == 'contact' else 'contact_id'
            query = ContactController.SELECT_QUERY.format(
                columns=target,
                table=table_name,
                filter=where
            )
            self.database.cursor.execute(query, values)
            results.append(set([item[0] for item in self.database.cursor.fetchall()]))

        # search words results
        for word in search_data['search_words']:
            if word:
                word_results = []
                for table_name, columns in self.SEARCH_RANGE.iteritems():
                    wheres = []
                    args = []
                    for column in columns:
                        wheres.append("{table}.{column} LIKE ?".format(table=table_name, column=column))
                        args.append(word)
                    where = " OR ".join(wheres)
                    target = 'id' if table_name == 'contact' else 'contact_id'
                    query = ContactController.SELECT_QUERY.format(
                        columns=target,
                        table=table_name,
                        filter=where
                    )
                    self.database.cursor.execute(query, args)
                    word_results.append(set([item[0] for item in self.database.cursor.fetchall()]))
                # merge all results for one word (OR)
                merged_word_results = list(itertools.chain.from_iterable(word_results))
                results.append(set(merged_word_results))

        # intersection of all results (AND)
        contact_ids = set.intersection(*results)

        # return contacts for contact_ids
        return self.select_contacts_for_ids(contact_ids)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                        UPDATE METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def update_contact(self, contact):
        """
        TBD
        :param contact: (dict) A dictionary that contains a valid contact structure
        :return:
        """
        # json ist die gesamte contact struktur
        contact_id = contact["contact"]["id"]
        id_filter = "id={id}".format(id=contact_id)
        contact_id_filter = "contact_id={id}".format(id=contact_id)
        try:
            self._update_table("contact", contact["contact"], id_filter)
            for mail in contact["mail"]:
                self._update_table("mail", mail, contact_id_filter)
            for address in contact["address"]:
                self._update_table("address", address, contact_id_filter)
            for phone in contact["phone"]:
                self._update_table("phone", phone, contact_id_filter)
            for study in contact["study"]:
                self._update_table("study", study, contact_id_filter)
            self.database.commit()
        except BaseException, e:
            self.database.rollback()
            raise e
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                       DELETE METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    def delete_contact(self, contact):
        """
        Deletes a given contact structure. NOTE: This method expects a contact structure, not just a
        contact id!
        
        :param contact: (dict) The contact structure to delete
        :return: (None)
        """
        contact_id = contact["contact"]["id"]
        id_filter = "id={id}".format(id=contact_id)
        contact_id_filter = "contact_id={id}".format(id=contact_id)
        try:
            self._delete_json_in_table("contact", id_filter)
            self._delete_json_in_table("mail", contact_id_filter)
            self._delete_json_in_table("phone", contact_id_filter)
            self._delete_json_in_table("address", contact_id_filter)
            self._delete_json_in_table("study", contact_id_filter)
            self.database.commit()
        except BaseException, e:
            self.database.rollback()
            raise e
    
    def _select_named_data(self, columns, table, where=""):
        """
        Select data from a given table and return a labeled data set
        
        :param columns: ([str]) A list of columns to select (NOTE: to select all columns, pass ["*"])
        :param table: (str) Table to select from
        :param where: (str) A valid mysqlite3 WHERE clause. NOTE: if no filter is necessary, you can omit the argument
        :return: ([dict]) A list of selected data as column/value pairs
        """
        if columns == ["*"]:
            # For correct return values replace "*" with list of column names
            columns = ContactController.TABLE_COLUMNS[table]
        columns_as_string = ",".join(columns)
        if not where:
            query = ContactController.SELECT_QUERY_NO_WHERE.format(
                columns=columns_as_string,
                table=table
            )
        else:
            query = ContactController.SELECT_QUERY.format(
                columns=columns_as_string,
                table=table,
                filter=where
            )
        self.database.cursor.execute(query)
        result = [dict(zip(columns, data)) for data in self.database.cursor.fetchall()]
        return result
    
    def _insert_json_in_table(self, row, table, commit=False):
        """
        Inserts a dict containing column/value pairs into a given table
        
        :param row: (dict) The data to insert into 'table'
        :param table: (str) The table name to insert the data in
        :param commit: (bool) If True, this method will automatically commit all changes
        :return: (int) The ID of the last row inserted
        """
        columns = row.keys()
        if ContactController._columns_are_invalid_for_table(columns, table):
            raise ValueError("Invalid columns: {columns}".format(columns=columns))
        values = row.values()
        query = ContactController.INSERT_QUERY.format(
            table=table,
            columns=",".join(columns),
            placeholders=",".join(list("?"*len(columns)))
        )
        self.database.cursor.execute(query, values)
        if commit:
            self.database.commit()
        return self.database.cursor.lastrowid
    
    def _update_table(self, table, data, where, commit=False):
        """
        Interface to sqlite3 UPDATE TABLE query for contact data structure.

        :param table: (str) Contact table to update (contact, mail, phone, address or study)
        :param data: ({str: str}) key/value pairs of data to update
        :param where: (str) Which records should be updated? (Standard would be 'contact_id=<id>')
        :param commit: (bool) Commit changes within function call
        :return: (none)
        """
        columns = filter(lambda col: col in ContactController.TABLE_COLUMNS[table] ,data.keys())
        updates = ",".join(["{column}=?".format(column=column) for column in columns])
        query = ContactController.UPDATE_QUERY.format(
            table=table,
            updates=updates,
            filter=where
        )
        args = data.values()
        self.database.cursor.execute(query, args)
        if commit:
            self.database.commit()
    
    def delete_by_id(self, table, id, commit=False):
        if table == "contact":
            primary = "id"
        else:
            primary = "contact_id"
        query = ContactController.DELETE_BY_ID_QUERY.format(
            table=table,
            id=primary
        )
        args = (id,)
        self.database.cursor.execute(query, args)
        if commit:
            self.database.commit()
    
    def _delete_json_in_table(self, table, where, commit=False):
        query = ContactController.DELETE_QUERY.format(
            table=table,
            filter=where
        )
        self.database.cursor.execute(query)
        if commit:
            self.database.commit()

# for simple tests
if __name__ == "__main__":
    from backend.database.Database import Database
    import logging
    path = "../../../myDatabase.db"
    d = Database(path, logging.getLogger("test"))
    ctr = ContactController(d)
    search_data = {
        'search_words': ['daniel'],
        'filter': [
            {'table': 'contact', 'column': 'prefix', 'values': ['Frau']}
        ]
    }
    results = ctr.select_contacts_by_search(search_data)
    print "done"
    for contact in results:
        for row in contact.items():
            print row
        print "\n"
