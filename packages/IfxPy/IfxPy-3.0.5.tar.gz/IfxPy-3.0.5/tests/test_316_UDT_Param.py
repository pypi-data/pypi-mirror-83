#

#

#

import unittest, sys, os
import IfxPy
#need to add this line below to each file to make the connect parameters available to all the test files
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_316_UDT_Param(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_316)

  def run_test_316(self):
    # Make a connection
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)

    # Get the server type
    server = IfxPy.server_info( conn )

    try:
        sql = "drop table rc_create;"
        stmt = IfxPy.exec_immediate(conn, sql)
    except:
        pass

    sql = "DROP ROW TYPE if exists details RESTRICT;"
    IfxPy.exec_immediate(conn, sql)

    sql = "DROP ROW TYPE if exists udt_t1 RESTRICT;"
    IfxPy.exec_immediate(conn, sql)

    sql = " create ROW type details(name varchar(15), addr varchar(15), zip varchar(15) );"
    stmt = IfxPy.exec_immediate(conn, sql)

    sql = " create ROW type udt_t1(name varchar(20), zip int);"
    stmt = IfxPy.exec_immediate(conn, sql)

    sql = "create table rc_create (c1 int, c2 SET(CHAR(10)NOT NULL), c3 MULTISET(int not null), c4 LIST(int not null), c5 details, c6 udt_t1 );"
    stmt = IfxPy.exec_immediate(conn, sql)

    #sql = "INSERT INTO rc_create(c1, c2) values(?, ?);"
    sql = "INSERT INTO rc_create VALUES (?, ?, ?, ?, ?, ?);"
    stmt = IfxPy.prepare(conn, sql)

    c1 = None
    c2 = None
    c3 = None
    c4 = None    
    c5 = None
    c6 = None

    IfxPy.bind_param(stmt, 1, c1, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_INTEGER)
    IfxPy.bind_param(stmt, 2, c2, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_CHAR, IfxPy.SQL_INFX_RC_COLLECTION) 
    IfxPy.bind_param(stmt, 3, c3, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_CHAR, IfxPy.SQL_INFX_RC_COLLECTION)
    IfxPy.bind_param(stmt, 4, c4, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_CHAR, IfxPy.SQL_INFX_RC_COLLECTION)
    IfxPy.bind_param(stmt, 5, c5, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_CHAR, IfxPy.SQL_INFX_UDT_FIXED)
    IfxPy.bind_param(stmt, 6, c6, IfxPy.SQL_PARAM_INPUT, IfxPy.SQL_CHAR, IfxPy.SQL_INFX_UDT_VARYING)
    i = 0
    while i < 3:
        i += 1
        c1 = 100+i
        c2 = "SET{'test', 'test1'}"
        c3 = "MULTISET{1,2,3}"
        c4 = "LIST{10, 20}"
        c5 = "ROW('Pune', 'City', '411061')"
        c6 = "ROW('Mumbai', 11111)"
        IfxPy.execute(stmt, (c1, c2, c3, c4, c5, c6));
   

    sql = "SELECT * FROM rc_create"
    stmt = IfxPy.exec_immediate(conn, sql)
    tu = IfxPy.fetch_tuple(stmt)

    print ("UDT Param complete")

#__END__
#__LUW_EXPECTED__
#UDT Param complete
#__ZOS_EXPECTED__
#UDT Param complete
#__SYSTEMI_EXPECTED__
#UDT Param complete
#__IDS_EXPECTED__
#UDT Param complete
