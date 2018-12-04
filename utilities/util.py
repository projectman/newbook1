"""
@package utilities

Util class implementation
All most commonly used utilities should be implemented in this class

Example:
    name = self.util.getUniqueName()
"""
import time
import traceback
import random, string
import utilities.custom_logger as cl
import logging

class Util(object):

    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of time
        """
        if info is not None:
            self.log.info("Wait :: '" + str(sec) + "' seconds for " + info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        """
        Get random string of characters

        Parameters:
            length: Length of string, number of characters string should have
            type: Type of characters string should have. Default is letters
            Provide lower/upper/digits for different types
        """
        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        """
        Get a unique name
        """
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, list_size=5, item_length=None):
        """
        Get a list of valid email ids

        Parameters:
            list_size: Number of names. Default is 5 names in a list
            item_length: It should be a list containing number of items equal to the listSize
                        This determines the length of the each item in the list -> [1, 2, 3, 4, 5]
        """
        nameList = []
        for i in range(0, list_size):
            nameList.append(self.getUniqueName(item_length[i]))
        return nameList

    def verifyTextContains(self, expected_text, actual_text):
        """
        Verify actual text contains expected text string
        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
        self.log.info("Expected Text From Application Web UI --> :: " + expected_text)
        if expected_text.lower() in actual_text.lower():
            self.log.info("### VERIFICATION CONTAINS !!! Actual Text "
                          + actual_text + " contains expected text: " + expected_text)
            return True
        else:
            self.log.error("### VERIFICATION DOES NOT CONTAINS !!!")
            return False

    def verifyTextMatch(self, actual_text, expected_text):
        """
        Verify text match

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
        self.log.info("Expected Text From Application Web UI --> :: " + expected_text)
        if actual_text.lower() == expected_text.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.error("### VERIFICATION DOES NOT MATCHED !!!")
            return False

    def verifyListMatch(self, expected_list, actual_list):
        """
        Verify two list matches

        Parameters:
            expected_list: Expected List
            actual_list: Actual List
        """
        return set(expected_list) == set(actual_list)

    def verifyListContains(self, expectedList, actualList):
        """
        Verify actual list contains elements of expected list

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True

    def verifyNumbersMatch(self, expected_num, actual_num):
        """
            Return True, if the expected_num is equal actual_num.
            In other case: False.
        """
        res = (expected_num == actual_num)
        if res:
            self.log.info(("Expected number: " + str(expected_num) +
                           " is equal actual number: " + str(actual_num)))
        else:
            self.log.error(("Expected number: " + str(expected_num) +
                            " is NOT equal actual number: " + str(
                        actual_num)))
        return res

    def absentFalseInList(self, list_in):
        """
        Return False if in the list_in (list of booleans)
        will be found one False. In other case return True.
        """
        try:
            if all(list_in) and len(list_in) > 0:
                self.log.info(("In incoming list only True: "
                               + str(list_in)))
                return True

            else:
                self.log.info(("In incoming list has False or lenght == 0 : "
                               + str(list_in)))
                return False
        except:
            self.log.error(("Incoming argument list_in is not sequence: "
                            + str(list_in)))
            return False

    def randomIndexList(self, size_of_range, out_list_size):
        """
        Function that takes size_of_range, out_list_size <- 2 integers.
        # create range of indexes length with size of range.
        # shuffle them and took first out_list_size elements.
        """
        index_list = list(range(size_of_range))
        random.shuffle(index_list)
        result = index_list[:out_list_size]
        self.log.info(("Found random list of indexes: " + str(result)))
        return result



