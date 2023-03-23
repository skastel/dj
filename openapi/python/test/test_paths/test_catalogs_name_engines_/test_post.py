# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import djopenapi
from djopenapi.paths.catalogs_name_engines_ import post  # noqa: E501
from djopenapi import configuration, schemas, api_client

from .. import ApiTestMixin


class TestCatalogsNameEngines(ApiTestMixin, unittest.TestCase):
    """
    CatalogsNameEngines unit test stubs
        Add Engines To Catalog  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = post.ApiForpost(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 201






if __name__ == '__main__':
    unittest.main()
