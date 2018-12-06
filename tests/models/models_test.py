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
        There are 7 items for "Filter by Category" on Models Page.
        """
        res = self.mp.actualCategoriesNumEqualExpected()  # TC # 018

        self.ts.markFinal(
            "TC #018 There must be 7 items for 'Filter by Category' "
            "on Models Page. ",
            res, ": TC #018 TOTALLY FAILED test_elementsAvailable.")

    def test_galeryRowsAvailable(self):
        """ Check models gallery rows available on Models page
        There are more than 5 (data.json:"minimal_number_rows";
         rows of model's gallery on page. TC # 019
        """

        res = self.mp.verifyRows()

        self.ts.markFinal(
            "TC #019 There must be more ro equal 5 rows in gallery"
            "on Models Page. ",
            res, ": TC #019 TOTALLY FAILED test_galeryRowsAvailable.")

    def test_verifyCategories(self):
        """ Check the every category is filtering on Models Page
        There are more than 5 rows of model's gallery on page. TC # 019
        """
        # !!! switch on all elements of classes list.
        res = self.mp.verifyCategoriesUrls()
        self.ts.markFinal(
            "TC #020 Check the every category is filtering on Models Page"
            "on Models Page. ",
            res[0] , (": TC #020 TOTALLY FAILED test_verifyCategories. "
                      + str(res[1])))

    def test_verifyNumberAvatars(self):
        """
        Check that all models have avatar in row. TC # 021.
        """

        res = self.mp.verifyNumberAvatars()
        self.ts.markFinal(
            "TC #021 Check the number of avatars on Models Page",
            res, ": TC #021 TOTALLY FAILED test_verifyNumberAvatars. ")

    def test_verifyEveryAvatar(self):
        """
        Check that all models have avatar in row. TC # 022.
        number of avatars for checking described by data.json:"number_avatars";
        """
        result = self.mp.verifyEachAvatars()

        self.ts.markFinal(
            "TC #022 Check the every category is filtering on Models Page",
            result,
            ": TC #022 test_verifyEveryAvatar TOTALLY "
            "FAILED test_verifyEveryAvatar.")

    def test_verifyAllModelsHasImages(self):
        """
        Check randomly chosen 5 models has all 4 images in gallery row;
        1. Check 10 images in rows of one Model's gallery
        Verify first 10 images that they are availble.
        This number described by key "number_images_checking' in data.json
        images (neither more nor less). TC # 023.
        """

        res = self.mp.verifyNumberImagesRow()
        self.ts.markFinal(
            "TC #023 Check first 12 images on Models Page, they are clickable",
            res,": TC #023. test_verifyAllModelsHasImages TOTALLY FAILED. ")

    def test_verifyBookModels(self):
        """
        Check the randomly 3 models can be clicked by "Book model".

        """
        res = self.mp.verifyBookModelButton() # TC # 024
        self.ts.markFinal(
        "TC #024 Check first 3 Models' 'Book Model' button on Models Page, ",
            res, ": TC #024. test_verifyBookModels TOTALLY FAILED.")

    def test_verifyFavoriteButton(self):
        """
        Check randomly for 3 models can be clicked by "Favorite".

        """
        res = self.mp.verifyFavoriteButtons() #  TC # 025.
        self.ts.markFinal(
            "TC #025 Check the first 3 models can be clicked by 'Favorite', ",
            res, ": TC #025. test_verifyFavoritesButton TOTALLY FAILED. ")

    def test_verifyPortfolioButton(self):
        """
        Check the randomly chosen 3 models (data.json:"portfolio_num")
        can be clicked by "Favorite".

        """
        res = self.mp.verifySeePortfolioButton() # TC # 026
        self.ts.markFinal(
            "TC #026 Check randomly chosen 3 models can be "
            "clicked by 'Profile' button, ",
            res, ": TC #026. test_verifyPortfolioButton TOTALLY FAILED. ")
