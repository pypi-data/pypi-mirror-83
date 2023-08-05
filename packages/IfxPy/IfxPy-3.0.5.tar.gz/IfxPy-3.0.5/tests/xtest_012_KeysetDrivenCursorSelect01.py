# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_012_KeysetDrivenCursorSelect01(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_012)

  def run_test_012(self):
      conn = IfxPy.connect(config.ConnStr, config.user, config.password)
      
      if conn:
        serverinfo = IfxPy.server_info( conn )
        if (serverinfo.DBMS_NAME[0:3] != 'Inf'):
          stmt = IfxPy.prepare(conn, "SELECT name FROM animals WHERE weight < 10.0", {IfxPy.SQL_ATTR_CURSOR_TYPE: IfxPy.SQL_CURSOR_KEYSET_DRIVEN})
        else:
          stmt = IfxPy.prepare(conn, "SELECT name FROM animals WHERE weight < 10.0")
        IfxPy.execute(stmt)
        data = IfxPy.fetch_both( stmt )
        while (data):
          print(data[0])
          data = IfxPy.fetch_both( stmt)
        IfxPy.close(conn)
      else:
        print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Pook            
#Bubbles         
#Gizmo           
#Rickety Ride    
#__ZOS_EXPECTED__
#Pook            
#Bubbles         
#Gizmo           
#Rickety Ride    
#__SYSTEMI_EXPECTED__
#Pook            
#Bubbles         
#Gizmo           
#Rickety Ride    
#__IDS_EXPECTED__
#Pook            
#Bubbles         
#Gizmo           
#Rickety Ride    
