#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from passlib.hash import pbkdf2_sha256


class PasshashVerifier(object):

    @staticmethod
    def verify(password, salt, passhash):
        return pbkdf2_sha256.verify(salt + password, passhash)
