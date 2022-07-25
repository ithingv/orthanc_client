import unittest
import pytest_check as check
from orthanc_cli import utils


class DCMWebUtilTests(unittest.TestCase):
    """class is needed to handle exceptions"""

    def test_validate_host_str(self):
        """url should be validated"""
        test_url = "https://valid.url"
        with self.assertRaises(ValueError):
            utils.validate_host_str('invalid url')
        assert utils.validate_host_str(test_url) \
            == "https://valid.url/"

    
    def test_validate_path(self):
        """path should be validated"""
        assert utils.validate_path("studies/1") == "studies/1"
        assert utils.validate_path("/studies/1") == "studies/1"
        assert utils.validate_path("studies/1/") == "studies/1"
        assert utils.validate_path("/studies/1/") == "studies/1"
        assert utils.validate_path(
            "/studies/1/series/1/instances/1") == "studies/1/series/1/instances/1"
        with self.assertRaises(ValueError):
            # path_splitted[-2] not in ["root", "studies", "series", "instances", "frames"]:
            utils.validate_path("/asdas/1")
            utils.validate_path('/')

    
    def test_get_dicom_tag(self):
        """ids should be reached by tags"""
        sample_tags = {
            utils.STUDY_TAG: {
                "Value" : ["1"]
            },
            utils.SERIES_TAG: {
                "Value" : ["2"]
            },
            utils.INSTANCE_TAG: {
                "Value" : ["3"]
            }
        }
        assert utils.get_dicom_tag(sample_tags, utils.STUDY_TAG) == "1"
        assert utils.get_dicom_tag(sample_tags, utils.SERIES_TAG) == "2"
        assert utils.get_dicom_tag(sample_tags, utils.INSTANCE_TAG) == "3"
        with self.assertRaises(LookupError):
            utils.get_dicom_tag(sample_tags, "notag")    


    def test_get_path_level():
        """should get correct level"""
        check.equal(utils.get_path_level(
            utils.ids_from_path("/"), 
        ))
