#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import itertools

from backend.database.controller.BaseController import BaseController


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
    
    CONTACT_PROFILE = {
        'primary': {'table': 'contact', 'column': 'id'},
        'rows': {
            'mail': {'key': 'contact_id', 'multiple': True},
            'phone': {'key': 'contact_id', 'multiple': True},
            'address': {'key': 'contact_id', 'multiple': True},
            'study': {'key': 'contact_id', 'multiple': True},
            'member': {'key': 'contact_id', 'multiple': False}
        }
    }

    # TODO: Export to BaseController
    SELECT_QUERY = "SELECT {columns} FROM `{table}` WHERE {filter};"
    SELECT_QUERY_NO_WHERE = "SELECT {columns} FROM `{table}`;"
    INSERT_QUERY = "INSERT INTO `{table}` ({columns}) VALUES ({placeholders});"
    UPDATE_QUERY = "UPDATE `{table}` SET {updates} WHERE {filter};"
    DELETE_QUERY = "DELETE FROM `{table}` WHERE {filter};"
    DELETE_BY_ID_QUERY = "DELETE FROM `{table}` WHERE {id}=?;"
    QUERY_SELECT_ALL_CONTACT_IDS = "SELECT id FROM `contact`;"
    
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
        self.base = BaseController
    
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
        return self.base.create_profile(ContactController.CONTACT_PROFILE, contact, commit)

    def create_contacts(self, contacts):
        """
        Expects a list of contact structures and calls create_contact() on each of them.
        
        :param contacts: ([dict]) A list of contact structures
        :return: ([int]) A list of the respective contact ids
        """
        return self.base.create_profiles(ContactController.CONTACT_PROFILE, contacts)
    
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
        return self.base.select_profile_for_id(contact_id)
    
    def select_contacts_for_ids(self, contact_ids):
        """
        Select multiple contact structures for a given list of IDs.
        
        :param ids: ([int]) List of contact ids to fetch from the database
        :return: ([dict]) A list of matching contact structures (can contain empty dicts for not matching IDs)
        """
        return self.base.select_profiles_for_ids(contact_ids)
    
    def select_all_contact_ids(self):
        """
        Selects all existing contact IDs from the database.
        
        :return: ([int]) A list of all existing contact IDs
        """
        return self.base.select_all_profile_ids(ContactController.CONTACT_PROFILE)
    
    def select_all_contacts(self):
        """
        Calls select_contacts_for_ids with select_all_contact_ids() as argument.
        
        :return: ([dict])  A list of all contact structures
        """
        return self.base.select_all_profiles(ContactController.CONTACT_PROFILE)
    
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
    def select_contacts_by_search(self, json):
        # TODO: NOT IMPLEMENTED YET
        pass
    
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
