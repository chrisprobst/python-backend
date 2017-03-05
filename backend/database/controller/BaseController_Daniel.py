#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import

class BaseController(object):

    def __init__(self, database):
        self.database = database

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                        CREATE METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def create_profile(self, profile, data, commit=True):
        """
        Creates a new profile in the database given a data structure. Note: since this profile is
        new, no "id" field in the data is required.

        :param profile: (dict) A profile definition
        :param data: (dict) A data structure for the profile (no IDs required!)
        :param commit: (bool) If true, all changes will be committed at the end of the function call
        :return: (int) The generated profile id for the new profile record
        """
        try:
            primary_table = profile['primary']['table']
            profile_key = self._insert_json_in_table(data[primary_table], primary_table)
            for table, row in profile['rows']:
                if not row['multiple']:
                    data[table][0] = data[table]
                for element in data[table]:
                    key = profile['rows'][table]['key']
                    element[key] = profile_key
                    self._insert_json_in_table(element, table)
            if commit:
                self.database.commit()
            return profile_key
        except BaseException, e:
            self.database.rollback()
            raise e

    def create_profiles(self, profile, data):
        """
        Expects a list of profile structures and calls create_profile() on each of them.

        :param profile: (dict) A profile definition
        :param data: ([dict]) A list of profile structures
        :return: ([int]) A list of the respective profile ids
        """
        profile_ids = []
        try:
            for single_profile in data:
                new_profile_id = self.create_profile(profile, single_profile, commit=False)
                profile_ids.append(new_profile_id)
            self.database.commit()
            return profile_ids
        except BaseException, e:
            self.database.rollback()
            raise e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                        READ METHODS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def select_profile_for_id(self, profile_id):
        """
        Select a profile structure from database for a given ID.

        :param profile_id: (int) The profile id to fetch from the database
        :return: (dict) The matching profile structure or an empty dictionary
        """
        id_filter = "id={id}".format(id=profile_id)
        profile_id_filter = "profile_id={id}".format(id=profile_id)
        result_profile = self._select_named_data(["*"], "profile", id_filter)
        result_mail = self._select_named_data(["*"], "mail", profile_id_filter)
        result_phone = self._select_named_data(["*"], "phone", profile_id_filter)
        result_address = self._select_named_data(["*"], "address", profile_id_filter)
        result_study = self._select_named_data(["*"], "study", profile_id_filter)
        if len(result_profile) != 1:
            return {}
        profile = {
            "profile": result_profile[0],
            "mail": result_mail,
            "phone": result_phone,
            "address": result_address,
            "study": result_study
        }
        return profile

    def select_profiles_for_ids(self, profile_ids):
        """
        Select multiple profile structures for a given list of IDs.

        :param ids: ([int]) List of profile ids to fetch from the database
        :return: ([dict]) A list of matching profile structures (can contain empty dicts for not matching IDs)
        """
        profiles = []
        for profile_id in ids:
            profiles.append(self.select_profile_for_id(profile_id))
        return profiles

    def select_all_profile_ids(self, profile):
        """
        Selects all existing profile IDs from the database.

        :return: ([int]) A list of all existing profile IDs
        """
        self.database.cursor.execute(BaseController.QUERY_SELECT_ALL_CONTACT_IDS)
        profile_ids = [result[0] for result in self.database.cursor.fetchall()]
        return profile_ids

    def select_all_profiles(self, profile):
        """
        Calls select_profiles_for_ids with select_all_profile_ids() as argument.

        :return: ([dict])  A list of all profile structures
        """
        profile_ids = self.select_all_profile_ids()
        return self.select_profiles_for_ids(profile_ids)
