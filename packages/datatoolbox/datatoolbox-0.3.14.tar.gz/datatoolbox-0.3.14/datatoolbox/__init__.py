#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
----------- DATA TOOL BOX -------------
This is a python tool box project for handling global datasets. It contains the following features:

    Augumented pandas DataFrames adding meta data,
    Automatic unit conversion and table based computations
    ID based data structure

Authors: Andreas Geiges  
         Gaurav Ganti

@Climate Analytics gGmbH
"""

from .version import version as __version__

import os
import time
import copy
from . import config
from . import core
from .data_structures import Datatable, TableSet, read_csv

from . import database
core.DB = database.Database()
from . import mapping as mapp
from . import io_tools as io
from . import interfaces
from . import util as util
from . import admin as admin

from . import rawSources as _raw_sources

# Predefined sets for regions and scenrarios
from datatoolbox.sets import REGIONS, SCENARIOS

# unit conversion package
unitReg = core.ur

ExcelReader = io.ExcelReader # TODO make this general IO tools

commitTable  = core.DB.commitTable
commitTables = core.DB.commitTables

updateTable  = core.DB.updateTable
updateTables = core.DB.updateTables

removeTable  = core.DB.removeTable
removeTables  = core.DB.removeTables

find         = core.DB.getInventory
findp        = core.DB.findp
findExact    = core.DB.findExact
getTable     = core.DB.getTable
getTables    = core.DB.getTables

isAvailable  = core.DB._tableExists

updateExcelInput = core.DB.updateExcelInput

insertDataIntoExcelFile = io.insertDataIntoExcelFile
sources = _raw_sources.sources

getCountryISO = util.getCountryISO

conversionFactor = core.conversionFactor

# extract data for specific countries and sources
countryDataExtract = util.getCountryExtract

executeForAll = util.forAll

DBinfo = core.DB.info
sourceInfo = core.DB.sourceInfo
inventory = core.DB.returnInventory

validate_ID = core.DB.validate_ID
#writeMAGICC6ScenFile = tools.wr

# Source management
import_new_source_from_remote = core.DB.importSourceFromRemote
export_new_source_to_remote   = core.DB.exportSourceToRemote
remove_source                 = core.DB.removeSource
push_source_to_remote         = core.DB.gitManager.push_to_remote_datashelf
pull_source_from_remote      = core.DB.gitManager.pull_update_from_remote

import datatoolbox.tools as tools

if config.PATH_TO_DATASHELF == os.path.join(config.MODULE_PATH, 'data/SANDBOX_datashelf'):
    print("""
          ################################################################
          You are using datatoolbox with a testing database as a SANDBOX.
          This allows for testing and initial tutorial use.
          

          For creating an empty dataase please use:
              "datatoolbox.admin.create_empty_datashelf(pathToDatabase)"

          For switching to a existing database use: 
              "datatoolbox.admin.change_personal_config()"
              
              
          ################################################################
          """)
