import utilities.custom_logger as cl
import logging
from base.selenium_driver import SeleniumDriver
from traceback import print_stack

class StatusDisplay (SeleniumDriver):

    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):

        super(StatusDisplay, self).__init__(driver)
        self.result_list = []

    def setResult(self, result, result_message):
        try:
            if result is not None:
                if result:
                    self.result_list.append( "PASS" )
                    self.log.info(
                        "### VERIFICATION SUCCESSFULL :: +  " + str(result_message))
                else:
                    self.result_list.append("FAIL")
                    self.log.info("### VERIFICATION FAILED :: + " + str(result_message))
                    self.screenShot(result_message)
            else:
                self.result_list.append("FAIL")
                self.log.info("### VERIFICATION FAILED :: + " + str(result_message))
                self.screenShot( result_message )
        except:
            self.result_list.append("FAIL")
            self.log.info("### EXEPTION OCCURED!!!")
            self.screenShot( result_message )
            print_stack()

    def mark(self, result, result_message):
        """
        Mark the result of the verification point in a test case.
        """
        print ("enter in mark")
        self.setResult(result, result_message)

    def markFinal(self, test_name, result, result_message):
        """
        Mark the final rusult of the verification point in a test case
        this needs to be called at least onece in a test case
        This should be final test status of the test case.
        """
        print( "enter in markFinal" )
        self.setResult(result, result_message)

        if "FAIL" in self.result_list:
            self.log.info( test_name, "### TEST FAILED.", result_message )
            self.result_list.clear()
            assert False
        else:
            self.log.info( test_name, "+ SUCCESSFUL." )
            self.result_list.clear()
            assert True


