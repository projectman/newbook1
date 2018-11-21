import utilities.custom_logger as cl
import logging
from base.main_driver import MainDriver
from traceback import print_stack

class StatusDisplay (MainDriver):

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):

        super(StatusDisplay, self).__init__(driver)
        self.result_list = []

    def setResult(self, result, test_name):
        try:
            if result is not None:
                if result:
                    self.result_list.append( "PASS" )
                    self.log.info(
                        "### TEST PASSED SUCCESSFUL : " + str(test_name))
                else:
                    self.result_list.append("FAIL")
                    self.log.error("### TEST FAILED as False: " + str(test_name))
                    self.screenShot(test_name)
            else:
                self.result_list.append("FAIL")
                self.log.error("### TESTS FAILED as None: " + str(test_name))
                self.screenShot(test_name)
        except:
            self.result_list.append("FAIL")
            self.log.error("### EXEPTION OCCURED!!!")
            self.screenShot(test_name)
            # print_stack()

    def mark(self, result, test_name):
        """
        Mark the result of the verification point in a test case.
        """
        self.setResult(result, test_name)

    def markFinal(self, test_name, result, problem_discription):
        """
        Mark the final rusult of the verification point in a test case
        this needs to be called at least onece in a test case
        This should be final test status of the test case.
        """
        self.log.info(("result on enter in markFinal is: " + str(result)))
        self.setResult(result, test_name)

        if "FAIL" in self.result_list:
            self.log.error(test_name + ": FULL TEST FAILED: "
                           + problem_discription)
            self.result_list.clear()
            assert False
        else:
            self.log.info(str(test_name) + ": FULL TEST SUCCESSFUL")
            self.result_list.clear()
            assert True

    
