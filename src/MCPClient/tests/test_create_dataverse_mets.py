#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import os
import sys
import shutil

import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    os.path.abspath(os.path.join(THIS_DIR, '../lib/clientScripts')))

import dataverse

# List of dataverse metadata fixtures. We use a namedtuple to provide some
# structure to this index so that we can keep track of information regarding
# dataverse over time, e.g. dataverse version number, the date the dataset was
# created, and so forth.
DataverseMDIndex = namedtuple('DataverseMDIndex',
                              'dv_version created_date title source fname')

dv_1 = DataverseMDIndex("4.8.6",
                        "2016-03-10T14:55:44Z",
                        "Test Dataset",
                        "https://demo.dataverse.org/dataset.xhtml?persistent"
                        "Id=doi:10.5072/FK2/XSAZXH",
                        "demo.dataverse.org.doi.10.5072.1.json")

dv_2 = DataverseMDIndex("4.8.6",
                        "2018-05-16T17:54:01Z",
                        "Bala Parental Alienation Study: Canada, United "
                        "Kingdom, and Australia 1984-2012 [test]",
                        "https://demodv.scholarsportal.info/dataset.xhtml?"
                        "persistentId=doi:10.5072/FK2/UNMEZF",
                        "demo.dataverse.org.doi.10.5072.2.json")

dv_3 = DataverseMDIndex("4.8.6",
                        "2018-05-09T21:26:07Z",
                        "A study with restricted data",
                        "https://demodv.scholarsportal.info/dataset.xhtml?"
                        "persistentId=doi:10.5072/FK2/WZTJWN",
                        "demo.dataverse.org.doi.10.5072.3.json")

dv_4 = DataverseMDIndex("4.8.6",
                        "2018-05-09T20:33:36Z",
                        "A study of my afternoon drinks ",
                        "https://demodv.scholarsportal.info/dataset.xhtml?"
                        "persistentId=doi:10.5072/FK2/6PPJ6Y",
                        "demo.dataverse.org.doi.10.5072.4.json")


class TestDataverseExample(object):

    write_dir = "fixtures/dataverse/dataverse_sources/mets/"
    fixture_path = "fixtures/dataverse/dataverse_sources"

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    FIXTURES_DIR = os.path.join(THIS_DIR, fixture_path)
    WRITE_DIR = os.path.join(THIS_DIR, write_dir)

    @pytest.mark.skip(reason="Pytest needs to be updated for "
                             "these tests to work")
    @pytest.fixture(autouse=True)
    def setup_session(self):
        try:
            os.makedirs(self.write_dir)
        except OSError:
            # The folder will be removed as part of pytest tear-down following
            # yield.
            pass
        yield
        # TODO: Clear state once the tests have completed...
        shutil.rmtree(self.WRITE_DIR)

    @pytest.mark.skip(reason="Pytest needs to be updated for "
                             "these tests to work")
    @pytest.mark.parametrize(
        "fixture_path, fixture_name, mets_output_path, mets_name",
        [(FIXTURES_DIR, dv_1.fname,
          WRITE_DIR, "METS.{}.xml".format(dv_1.fname)),
         (FIXTURES_DIR, dv_2.fname,
          WRITE_DIR, "METS.{}.xml".format(dv_2.fname)),
         (FIXTURES_DIR, dv_3.fname,
          WRITE_DIR, "METS.{}.xml".format(dv_3.fname)),
         # dv_4 is from the API, wheras 1, 2, 3 are from the dataverse manual
         # download link... we need to understand what to do in this
         # situation
         (FIXTURES_DIR, dv_4.fname,
          WRITE_DIR, "METS.{}.xml".format(dv_4.fname)),
         ])
    def test_parse_dataverse(self,
                             fixture_path,
                             fixture_name,
                             mets_output_path,
                             mets_name):
        dataverse.map_dataverse(
            sip_dir=fixture_path, dataset_md_name=fixture_name,
            md_path=mets_output_path, md_name=mets_name)