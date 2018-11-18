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
        """Check all filter elements available on Models Page
        There are 7 items for "Filter by Category" on Models Page. TC # 018
        """
        print("Supertest begun!")
        res = self.mp.verify_7_categories()

        self.ts.markFinal(
            "TC #018 There must be 7 items for 'Filter by Category' "
            "on Models Page.:",
            res, ": TC #018 TOTALLY FAILED.")
