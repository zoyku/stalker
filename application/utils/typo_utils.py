# look up typo generator types

import string
import random
import whois as whois
from application import db
from application.models import User, KeywordTypo

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
vowels = "aeiouy"


class TypoUtils:
    @staticmethod
    def insertedKey(s):
        """Produce a list of keywords using the `inserted key' method
        """
        kwds = []

        for i in range(0, len(s)):
            for char in alphabet:
                kwds.append(s[:i + 1] + char + s[i + 1:])

        return kwds

    @staticmethod
    def skipLetter(s):
        """Produce a list of keywords using the `skip letter' method
        """
        kwds = []

        for i in range(1, len(s) + 1):
            kwds.append(s[:i - 1] + s[i:])

        return kwds

    @staticmethod
    def doubleLetter(s):
        """Produce a list of keywords using the `double letter' method
        """
        kwds = []

        for i in range(0, len(s) + 1):
            kwds.append(s[:i] + s[i - 1] + s[i:])

        return kwds

    @staticmethod
    def reverseLetter(s):
        """Produce a list of keywords using the `reverse letter' method
        """
        kwds = []

        for i in range(0, len(s)):
            letters = s[i - 1:i + 1:1]
            if len(letters) != 2:
                continue

            reverse_letters = letters[1] + letters[0]
            kwds.append(s[:i - 1] + reverse_letters + s[i + 1:])

        return kwds

    @staticmethod
    def wrongVowel(s):
        """Produce a list of keywords using the `wrong vowel' method (for soundex)
        """
        kwds = []

        for i in range(0, len(s)):
            for letter in vowels:
                if s[i] in vowels:
                    for vowel in vowels:
                        s_list = list(s)
                        s_list[i] = vowel
                        kwd = "".join(s_list)
                        kwds.append(kwd)

        return kwds

    @staticmethod
    def wrongKey(s):
        """Produce a list of keywords using the `wrong key' method
        """
        kwds = []

        for i in range(0, len(s)):
            for letter in alphabet:
                kwd = s[:i] + letter + s[i + 1:]
                kwds.append(kwd)

        return kwds

    @staticmethod
    def callToTypo(s):
        kwds = []
        kwds += TypoUtils.insertedKey(s)
        kwds += TypoUtils.wrongKey(s)
        kwds += TypoUtils.skipLetter(s)
        kwds += TypoUtils.doubleLetter(s)
        kwds += TypoUtils.reverseLetter(s)
        kwds += TypoUtils.wrongVowel(s)
        return kwds
