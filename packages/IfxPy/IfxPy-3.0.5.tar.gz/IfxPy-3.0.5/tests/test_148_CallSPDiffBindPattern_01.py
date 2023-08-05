# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_148_CallSPDiffBindPattern_01(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_148)

  def run_test_148(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    
    if conn:
      ##### Set up #####
      serverinfo = IfxPy.server_info( conn )
      server = serverinfo.DBMS_NAME[0:3]
      try:
          sql = "DROP TABLE sptb"
          IfxPy.exec_immediate(conn, sql)
      except:
          pass
      
      try:
          sql = "DROP PROCEDURE sp"
          IfxPy.exec_immediate(conn, sql)
      except:
          pass
      
      sql = "CREATE TABLE sptb (c1 INTEGER, c2 FLOAT, c3 VARCHAR(10), c4 INT8, c5 VARCHAR(20))"
      
      IfxPy.exec_immediate(conn, sql)
      
      sql = "INSERT INTO sptb (c1, c2, c3, c4, c5) VALUES (1, 5.01, 'varchar', 3271982, 'varchar data')"
      IfxPy.exec_immediate(conn, sql)
      
      sql = """CREATE PROCEDURE sp(OUT out1 INTEGER, OUT out2 FLOAT, OUT out3 VARCHAR(10), OUT out4 INT8, OUT out5 VARCHAR(20));
                 SELECT c1, c2, c3, c4, c5 INTO out1, out2, out3, out4, out5 FROM sptb; END PROCEDURE;"""
      IfxPy.exec_immediate(conn, sql)
      #############################

      ##### Run the test #####

      out1 = 0
      out2 = 0.00
      out3 = ""
      out4 = 0
      out5 = ""

      stmt, out1, out2, out3, out4, out5 = IfxPy.callproc(conn, 'sp', (out1, out2, out3, out4, out5))

      print("out 1:")
      print(out1)
      print("out 2:")
      print(out2)
      print("out 3:")
      print(out3)
      print("out 4:")
      print(out4)
      print("out 5:")
      print(out5)
      #############################
    else:
      print("Connection failed.")

#__END__
#__IDS_EXPECTED__
#out 1:
#1
#out 2:
#5.01
#out 3:
#varchar
#out 4:
#3271982
#out 5:
#varchar data
