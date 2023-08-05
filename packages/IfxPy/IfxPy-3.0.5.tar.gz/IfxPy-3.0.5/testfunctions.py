#//////////////////////////////////////////////////////////////////////////
# Copyright 2017-2020 OpenInformix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http ://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
#      Sathyanesh Krishnan
#
#//////////////////////////////////////////////////////////////////////////

import os
import sys
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import re
import glob
import inspect

import IfxPy
import config

class IfxPyTestFunctions(unittest.TestCase):
  #prepconn = IfxPy.connect(config.database, config.user, config.password)
  prepconn = IfxPy.connect(config.ConnStr, "", "")
  server = IfxPy.server_info(prepconn)
  IfxPy.close(prepconn)
  
  # See the tests.py comments for this function.
  def setUp(self):
    pass
 
  # This function captures the output of the current test file.
  def capture(self, func):
    buffer = StringIO()
    sys.stdout = buffer
    func()
    sys.stdout = sys.__stdout__
    var = buffer.getvalue()
    #print var # JS debug	
    var = var.replace('\n', '').replace('\r', '')
    return var
  

  # This function grabs the expected output of the current test function for IDS,
  #   located at the bottom of the current test file.
  def expected_IDS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__IDS_EXPECTED__')[-1].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput

  # This function grabs the expected output of the current test function for zOS,
  #   located at the bottom of the current test file.
  def expected_AS(self, fileName):
    fileHandle = open(fileName, 'r')
    fileInput = fileHandle.read().split('#__SYSTEMI_EXPECTED__')[-1].split('#__IDS_EXPECTED__')[0].replace('\n', '').replace('#', '')
    fileHandle.close()
    return fileInput
    
  # This function compares the captured outout with the expected out of
  #   the current test file.
  def assert_expect(self, testFuncName):
    callstack = inspect.stack(0)
    try:
      if (self.server.DBMS_NAME[0:2] == "AS"):
          self.assertEqual(self.capture(testFuncName), self.expected_AS(callstack[1][1]))
      elif (self.server.DBMS_NAME[0:3] == "Inf"):
          self.assertEqual(self.capture(testFuncName), self.expected_IDS(callstack[1][1]))
      else:
          self.assertEqual(self.capture(testFuncName), self.expected_LUW(callstack[1][1]))
      
    finally:
      del callstack

  # This function will compare using Regular Expressions
  # based on the servre
  def assert_expectf(self, testFuncName):
    callstack = inspect.stack(0)
    try:
      if (self.server.DBMS_NAME[0:2] == "AS"):
          pattern = self.expected_AS(callstack[1][1])
      elif (self.server.DBMS_NAME[0:3] == "Inf"):
          pattern = self.expected_IDS(callstack[1][1])
      else:
          pattern = self.expected_LUW(callstack[1][1])
      
      sym = ['\[','\]','\(','\)']
      for chr in sym:
          pattern = re.sub(chr, '\\' + chr, pattern)

      pattern = re.sub('%s', '.*?', pattern)
      pattern = re.sub('%d', '\\d+', pattern)

      result = re.match(pattern, self.capture(testFuncName))
      self.assertNotEqual(result, None)
    finally:
      del callstack
      
  #def assert_throw_blocks(self, testFuncName):
  #  callstack = inspect.stack(0)
  #  try:

  # This function needs to be declared here, regardless of if there 
  #   is any body to this function
  def runTest(self):
    pass
