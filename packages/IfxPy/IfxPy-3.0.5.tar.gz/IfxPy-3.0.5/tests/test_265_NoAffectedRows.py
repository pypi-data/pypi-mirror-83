
import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_265_NoAffectedRows(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_265)

  def run_test_265(self):
    # Make a connection
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)

    cursor_option = {IfxPy.SQL_ATTR_CURSOR_TYPE: IfxPy.SQL_CURSOR_STATIC}

    if conn:
      server = IfxPy.server_info( conn )
      if (server.DBMS_NAME[0:3] == 'Inf'):
         op = {IfxPy.ATTR_CASE: IfxPy.CASE_UPPER}
         IfxPy.set_option(conn, op, 1)

      try:
        sql = 'drop table test'

        stmt = IfxPy.prepare(conn, sql)
        IfxPy.set_option(stmt, cursor_option, 0)
        IfxPy.execute(stmt)
        print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))
      except:
        pass

      if ((server.DBMS_NAME[0:3] == 'Inf') or (server.DBMS_NAME[0:2] == "AS")):
        sql = "create table test(id integer, name VARCHAR(10), text_col VARCHAR(100), some_var VARCHAR(100) )"
      else:
        sql = "create table test(id integer, name VARCHAR(10), text_col CLOB, some_var XML )"

      stmt = IfxPy.prepare(conn, sql)
      IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))

      sql = 'select id from test'

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))

      sql = "insert into test values( 1, 'some', 'here is a clob value', '<?xml version=\"1.0\" encoding=\"UTF-8\" ?><test attribute=\"value\"/>')"

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))

      sql = "insert into test values(2, 'value', 'clob data', NULL)"

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))

      sql = "insert into test values(2, 'in varchar', 'data2', NULL)"

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))

      sql = 'select * from test'

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))
      row = IfxPy.fetch_tuple(stmt)
      while ( row ):
        print("%s, %s, %s, %s\n" %(row[0], row[1], row[2], ((row[3] is not None) and row[3].startswith('\ufeff')) and  row[3][1:] or  row[3]))
        row = IfxPy.fetch_tuple(stmt)

      sql = 'select id, name from test where id = ?'

      stmt = IfxPy.prepare(conn, sql)
      #fx_db.set_option(stmt, cursor_option, 0)
      IfxPy.execute(stmt, (2,))
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))
      row = IfxPy.fetch_tuple(stmt)
      while ( row ):
        print("%s, %s\n" %(row[0], row[1]))
        row = IfxPy.fetch_tuple(stmt)

      if (server.DBMS_NAME[0:3] == 'Inf'):
        sql = "select * from test"
      else:
        sql = 'select * from test fetch first 12 rows only optimize for 12 rows'

      stmt = IfxPy.prepare(conn, sql)
      #IfxPy.set_option(stmt, cursor_option, 0)
      #IfxPy.num_fields(stmt)
      IfxPy.execute(stmt)
      print("Number of affected rows: %d" % IfxPy.get_num_result(stmt))
      row = IfxPy.fetch_tuple(stmt)
      while ( row ):
        print("%s, %s, %s, %s\n" %(row[0], row[1], row[2], ((row[3] is not None) and row[3].startswith('\ufeff')) and  row[3][1:] or  row[3]))
        row = IfxPy.fetch_tuple(stmt)

      IfxPy.close(conn)

#__END__
#__LUW_EXPECTED__
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: 0
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: -1
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#__ZOS_EXPECTED__
#Number of affected rows: -2
#Number of affected rows: -2
#Number of affected rows: 0
#Number of affected rows: -2
#Number of affected rows: -1
#Number of affected rows: -2
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#__SYSTEMI_EXPECTED__
#Number of affected rows: -2
#Number of affected rows: -2
#Number of affected rows: 0
#Number of affected rows: -2
#Number of affected rows: -1
#Number of affected rows: -2
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 0
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#__IDS_EXPECTED__
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: -1
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
#Number of affected rows: 2
#2, value
#2, in varchar
#Number of affected rows: 3
#1, some, here is a clob value, <?xml version="1.0" encoding="UTF-16" ?><test attribute="value"/>
#2, value, clob data, None
#2, in varchar, data2, None
