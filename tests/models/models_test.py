from utilities.statusdisplay import StatusDisplay
from pages.models.models_page import ModelsPage
import pytest
import time

@pytest.mark.usefixtures("oneTimeSetUp")
class TestModels:

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.mp = ModelsPage(self.driver)
        self.ts = StatusDisplay(self.driver)

    def test_elementsAvailable(self):
        """ Check all filter elements available on Models Page
        There are 7 items for "Filter by Category" on Models Page. TC # 018
        """
        number_of_categories = 7
        res = self.mp.verify_num_categories(number_of_categories)

        self.ts.markFinal(
            "TC #018 There must be 7 items for 'Filter by Category' "
            "on Models Page. ",
            res, ": TC #018 TOTALLY FAILED.")

    def test_galeryRowsAvailable(self):
        """ Check models gallery rows available on Models page
        There are more than 5 rows of model's gallery on page. TC # 019
        """
        number_of_rows = 5
        res = self.mp.verifyRows(number_of_rows)

        self.ts.markFinal(
            "TC #019 There must be more ro equal 5 rows in gallery"
            "on Models Page. ",
            res, ": TC #019 TOTALLY FAILED.")

    def test_verifyCategories(self):
        """ Check the every category is filtering on Models Page
        There are more than 5 rows of model's gallery on page. TC # 019
        """
        # !!! switch on all elements of classes list.
        res = self.mp.verifyCategoriesUrls()
        self.ts.markFinal(
            "TC #020 Check the every category is filtering on Models Page"
            "on Models Page. ",
            res[0] , (": TC #020 TOTALLY FAILED. " + str(res[1])))

    def test_verifyAllAvatars(self):
        """
        Check that all models have avatar in row. TC # 021.
        """

        res = self.mp.verifyAllHaveAvatars()
        self.ts.markFinal(
            "TC #021 Check the every category is filtering on Models Page"
            "on Models Page. ",
            res, ": TC #021 TOTALLY FAILED. " )
