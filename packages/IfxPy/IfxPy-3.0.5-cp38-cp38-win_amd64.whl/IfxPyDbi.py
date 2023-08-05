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
# +----------------------------------------------------------------------+
# | Authors: Sathyanesh Krishnan, Javier Sagrera, Rohit Pandey           |
# |                                                                      |
# +----------------------------------------------------------------------+
#
#//////////////////////////////////////////////////////////////////////////

# +--------------------------------------------------------------------------+
# | Authors: Swetha Patel, Abhigyan Agrawal, Tarun Pasrija, Rahul Priyadarshi,
# |          Akshay Anand, Saba Kauser
# +--------------------------------------------------------------------------+

"""
This module implements the Python DB API Specification v2.0 for Informix database.
"""

import types, string, time, datetime, decimal, sys
import weakref
from builtins import str

if sys.version_info >= (3, ):
   buffer = memoryview
if sys.version_info < (3, ):
   import exceptions
   exception = exceptions.Exception
else:
   exception = Exception

import IfxPy
__version__ = IfxPy.__version__

# Constants for specifying database connection options.
SQL_ATTR_AUTOCOMMIT = IfxPy.SQL_ATTR_AUTOCOMMIT
#SQL_ATTR_CURRENT_SCHEMA = IfxPy.SQL_ATTR_CURRENT_SCHEMA
SQL_AUTOCOMMIT_OFF = IfxPy.SQL_AUTOCOMMIT_OFF
SQL_AUTOCOMMIT_ON = IfxPy.SQL_AUTOCOMMIT_ON
ATTR_CASE = IfxPy.ATTR_CASE
CASE_NATURAL = IfxPy.CASE_NATURAL
CASE_LOWER = IfxPy.CASE_LOWER
CASE_UPPER = IfxPy.CASE_UPPER
SQL_FALSE = IfxPy.SQL_FALSE
SQL_TRUE = IfxPy.SQL_TRUE
SQL_TABLE_STAT = IfxPy.SQL_TABLE_STAT
SQL_INDEX_CLUSTERED = IfxPy.SQL_INDEX_CLUSTERED
SQL_INDEX_OTHER = IfxPy.SQL_INDEX_OTHER
SQL_DBMS_VER = IfxPy.SQL_DBMS_VER
SQL_DBMS_NAME = IfxPy.SQL_DBMS_NAME
USE_WCHAR = IfxPy.USE_WCHAR
WCHAR_YES = IfxPy.WCHAR_YES
WCHAR_NO = IfxPy.WCHAR_NO
FIX_RETURN_TYPE = 1

# Module globals
apilevel = '2.0'
threadsafety = 0
paramstyle = 'qmark'


class Error(exception):
    """This is the base class of all other exception thrown by this
    module.  It can be use to catch all exceptions with a single except
    statement.

    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        self._message = message
        super(Error, self).__init__(message)
    def __str__(self):
        """Converts the message to a string."""
        return 'IfxPyDbi::'+str(self.__class__.__name__)+': '+str(self._message)


class Warning(exception):
    """This exception is used to inform the user about important
    warnings such as data truncations.

    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        self._message = message
        super(Warning,self).__init__(message)
    def __str__(self):
        """Converts the message to a string."""
        return 'IfxPyDbi::'+str(self.__class__.__name__)+': '+str(self._message)


class InterfaceError(Error):
    """This exception is raised when the module interface is being
    used incorrectly.

    """
    pass


class DatabaseError(Error):
    """This exception is raised for errors related to database."""
    pass


class InternalError(DatabaseError):
    """This exception is raised when internal database error occurs,
    such as cursor is not valid anymore.

    """
    pass


class OperationalError(DatabaseError):
    """This exception is raised when database operation errors that are
    not under the programmer control occur, such as unexpected
    disconnect.

    """
    pass


class ProgrammingError(DatabaseError):
    """This exception is raised for programming errors, such as table 
    not found.

    """
    pass

class IntegrityError(DatabaseError):
    """This exception is thrown when errors occur when the relational
    integrity of database fails, such as foreign key check fails. 

    """
    pass


class  DataError(DatabaseError):
    """This exception is raised when errors due to data processing,
    occur, such as divide by zero. 

    """
    pass


class NotSupportedError(DatabaseError):
    """This exception is thrown when a method in this module or an 
    database API is not supported.

    """
    pass


def Date(year, month, day):
    """This method can be used to get date object from integers, for 
    inserting it into a DATE column in the database.

    """
    return datetime.date(year, month, day)

def Time(hour, minute, second):
    """This method can be used to get time object from integers, for 
    inserting it into a TIME column in the database.

    """
    return datetime.time(hour, minute, second)

def Timestamp(year, month, day, hour, minute, second):
    """This method can be used to get timestamp object from integers, 
    for inserting it into a TIMESTAMP column in the database.

    """
    return datetime.datetime(year, month, day, hour, minute, second)

def DateFromTicks(ticks):
    """This method can be used to get date object from ticks seconds,
    for inserting it into a DATE column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.date(time_tuple[0], time_tuple[1], time_tuple[2])

def TimeFromTicks(ticks):
    """This method can be used to get time object from ticks seconds,
    for inserting it into a TIME column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.time(time_tuple[3], time_tuple[4], time_tuple[5])

def TimestampFromTicks(ticks):
    """This method can be used to get timestamp object from ticks  
    seconds, for inserting it into a TIMESTAMP column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2], 
                                time_tuple[3], time_tuple[4], time_tuple[5])

def Binary(string):
    """This method can be used to store binary information, for 
    inserting it into a binary type column in the database.

    """
    if not isinstance( string, (bytes, memoryview) ):
        raise InterfaceError("Binary function expects type string argument.")
    return buffer(string)


class DBAPITypeObject(frozenset):
    """Class used for creating objects that can be used to compare
    in order to determine the python type to provide in parameter 
    sequence argument of the execute method.

    """
    def __new__(cls, col_types):
        return frozenset.__new__(cls, col_types)

    def __init__(self, col_types):
        """Constructor for DBAPITypeObject.  It takes a tuple of 
        database column type as an argument.
        """
        self.col_types = col_types

    def __cmp__(self, cmp):
        """This method checks if the string compared with is in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        if cmp in self.col_types:
            return 0
        if sys.version_info < (3, ):
            if cmp < self.col_types:
                return 1
            else:
                return -1
        else:
            return 1

    def __eq__(self, cmp):
        """This method checks if the string compared with is in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        return cmp in self.col_types

    def __ne__(self, cmp):
        """This method checks if the string compared with is not in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
        """
        return cmp not in self.col_types

    def __hash__(self):
        return id(self)

# The user can use these objects to compare the database column types
# with in order to determine the python type to provide in the 
# parameter sequence argument of the execute method.
STRING = DBAPITypeObject(("CHARACTER", "CHAR", "VARCHAR", 
                          "CHARACTER VARYING", "CHAR VARYING", "STRING",))

TEXT = DBAPITypeObject(("CLOB", "CHARACTER LARGE OBJECT", "CHAR LARGE OBJECT",))

# XML = DBAPITypeObject(("XML",))

BINARY = DBAPITypeObject(("BLOB", "BINARY LARGE OBJECT",))

NUMBER = DBAPITypeObject(("INTEGER", "INT", "SMALLINT",))

BIGINT = DBAPITypeObject(("BIGINT",))

FLOAT = DBAPITypeObject(("FLOAT", "REAL", "DOUBLE",))

DECIMAL = DBAPITypeObject(("DECIMAL", "DEC", "NUMERIC", "NUM",))

DATE = DBAPITypeObject(("DATE",))

TIME = DBAPITypeObject(("TIME",))

DATETIME = DBAPITypeObject(("TIMESTAMP",))

ROWID = DBAPITypeObject(())

# This method is used to determine the type of error that was
# generated.  It takes an exception instance as an argument, and
# returns exception object of the appropriate type.
def _get_exception(inst):
    # These tuple are used to determine the type of exceptions that are
    # thrown by the database.  They store the SQLSTATE code and the
    # SQLSTATE class code(the 2 digit prefix of the SQLSTATE code)
    warning_error_tuple = ('01', )
    data_error_tuple = ('02', '22', '10601', '10603', '10605', '10901', '10902', 
                                                               '38552', '54')

    operational_error_tuple = ( '08', '09', '10502', '10000', '10611', '38501', 
                          '38503', '38553', '38H01', '38H02', '38H03', '38H04',
                                   '38H05', '38H06', '38H07', '38H09', '38H0A')

    integrity_error_tuple = ('23', )

    internal_error_tuple = ('24', '25', '26', '2D', '51', '57')

    programming_error_tuple = ('08002', '07', 'OD', 'OF','OK','ON','10', '27',
                               '28', '2E', '34', '36', '38', '39', '56', '42',
                               '3B', '40', '44', '53', '55', '58', '5U', '21')

    not_supported_error_tuple = ('0A', '10509')

    # These tuple are used to determine the type of exceptions that are
    # thrown from the driver module. 
    interface_exceptions = (                  "Supplied parameter is invalid",
                                        "ATTR_CASE attribute must be one of "
                                    "CASE_LOWER, CASE_UPPER, or CASE_NATURAL",
                          "Connection or statement handle must be passed in.",
                                                       "Param is not a tuple")

    programming_exceptions = (                     "Connection is not active", 
                                                 "qualifier must be a string",
                                                   "unique must be a boolean",
                                                       "Parameters not bound",
                                                     "owner must be a string",
                                                "table_name must be a string",
                                                "table type must be a string", 
                                               "column_name must be a string", 
                                                "Column ordinal out of range", 
                                            "procedure name must be a string",
                              "Requested row number must be a positive value", 
                                     "Options Array must have string indexes")

    database_exceptions = (                                   "Binding Error", 
                                   "Column information cannot be retrieved: ", 
                                            "Column binding cannot be done: ",
                                             "Failed to Determine XML Size: ")

    statement_exceptions = (                     "Statement Execute Failed: ",
                                                    "Describe Param Failed: ",
                                                      "Sending data failed: ",
                                                            "Fetch Failure: ",
                                                  "SQLNumResultCols failed: ",
                                                       "SQLRowCount failed: ",
                                                   "SQLGetDiagField failed: ",
                                                 "Statement prepare Failed: ")

    operational_exceptions = (          "Connection Resource cannot be found", 
                                                  "Failed to Allocate Memory",
                                                    "Describe Param Failed: ",
                                                 "Statement Execute Failed: ",
                                                      "Sending data failed: ", 
                                     "Failed to Allocate Memory for XML Data",
                                     "Failed to Allocate Memory for LOB Data")

    # First check if the exception is from the database.  If it is
    # determine the SQLSTATE code which is used further to determine
    # the exception type.  If not check if the exception is thrown by
    # by the driver and return the appropriate exception type.  If it
    # is not possible to determine the type of exception generated
    # return the generic Error exception.
    if inst is not None:
        message = repr(inst)
        if message.startswith("Exception('") and message.endswith("',)"):
            message = message[11:]
            message = message[:len(message)-3]

        index = message.find('SQLSTATE=')
        if( message != '') & (index != -1):
            error_code = message[(index+9):(index+14)]
            prefix_code = error_code[:2]
        else:
            for key in interface_exceptions:
                if message.find(key) != -1:
                    return InterfaceError(message)
            for key in programming_exceptions:
                if message.find(key) != -1:
                    return ProgrammingError(message)
            for key in operational_exceptions:
                if message.find(key) != -1:
                    return OperationalError(message)
            for key in database_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)
            for key in statement_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)
            return Error(message)
    else:
        return Error('An error has occured')

    # First check if the SQLSTATE is in the tuples, if not check
    # if the SQLSTATE class code is in the tuples to determine the
    # exception type.
    if ( error_code in warning_error_tuple or 
         prefix_code in warning_error_tuple ):
        return Warning(message)
    if ( error_code in data_error_tuple or 
         prefix_code in data_error_tuple ):
        return DataError(message)
    if ( error_code in operational_error_tuple or 
         prefix_code in operational_error_tuple ):
        return OperationalError(message)
    if ( error_code in integrity_error_tuple or 
         prefix_code in integrity_error_tuple ):
        return IntegrityError(message)
    if ( error_code in internal_error_tuple or
         prefix_code in internal_error_tuple ):
        return InternalError(message)
    if ( error_code in programming_error_tuple or
         prefix_code in programming_error_tuple ):
        return ProgrammingError(message)
    if ( error_code in not_supported_error_tuple or
         prefix_code in not_supported_error_tuple ):
        return NotSupportedError(message)
    return DatabaseError(message)

def _server_connect(ConStr, user='', password='', host=''):
    """This method create connection with server
    """

    if ConStr is None:
        raise InterfaceError("ConStr value should not be None")

    if (not isinstance(ConStr, str)) | (not isinstance(user, str)) | (not isinstance(password, str)) | (not isinstance(host, str)):
        raise InterfaceError("Arguments should be of type string or unicode")

    # If the ConStr does not contain port and protocal adding database
    # and hostname is no good.  Add these when required, that is,
    # if there is a '=' in the ConStr.  Else the ConStr string is taken to be
    # a ConStr entry.
    if ConStr.find('=') != -1:
        if ConStr[len(ConStr) - 1] != ';':
            ConStr = ConStr + ";"
        if host != '' and ConStr.find('HOST=') == -1:
            ConStr = ConStr + "HOST=" + host + ";"

    # attach = true is not valid against IDS. And attach is not needed for connect currently.
    #if ConStr.find('attach=') == -1:
        #ConStr = ConStr + "attach=true;"
    if user != '' and ConStr.find('UID=') == -1:
        ConStr = ConStr + "UID=" + user + ";"
    if password != '' and ConStr.find('PWD=') == -1:
        ConStr = ConStr + "PWD=" + password + ";"
    try:
        conn = IfxPy.connect(ConStr, '', '')
    except Exception as inst:
        raise _get_exception(inst)

    return conn


def connect(ConStr, user='', password='', host='', database='', conn_options=None):
    """This method creates a non persistent connection to the database. It returns
        a IfxPyDbi.Connection object.
    """

    if ConStr is None:
        raise InterfaceError("connect expects a not None ConStr value") 

    if (not isinstance(ConStr, str)) | (not isinstance(user, str)) | (not isinstance(password, str)) | (not isinstance(host, str)) | (not isinstance(database, str)):
        raise InterfaceError("connect expects the first five arguments to"
                                                      " be of type string or unicode")
    if conn_options is not None:
        if not isinstance(conn_options, dict):
            raise InterfaceError("connect expects the sixth argument"
                                 " (conn_options) to be of type dict")
        if not SQL_ATTR_AUTOCOMMIT in conn_options:
            conn_options[SQL_ATTR_AUTOCOMMIT] = SQL_AUTOCOMMIT_OFF
    else:
        conn_options = {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_OFF}

    # If the ConStr does not contain port and protocal adding database
    # and hostname is no good.  Add these when required, that is,
    # if there is a '=' in the ConStr.  Else the ConStr string is taken to be
    # a ConStr entry.
    if ConStr.find('=') != -1:
        if ConStr[len(ConStr) - 1] != ';':
            ConStr = ConStr + ";"
        if database != '' and ConStr.find('DATABASE=') == -1:
            ConStr = ConStr + "DATABASE=" + database + ";"
        if host != '' and ConStr.find('HOST=') == -1:
            ConStr = ConStr + "HOST=" + host + ";"

    if user != '' and ConStr.find('UID=') == -1:
        ConStr = ConStr + "UID=" + user + ";"
    if password != '' and ConStr.find('PWD=') == -1:
        ConStr = ConStr + "PWD=" + password + ";"
    try:
        # conn = IfxPy.connect(ConStr, '', '', conn_options)
        conn = IfxPy.connect(ConStr, '', '')
        #IfxPy.set_option(conn, {SQL_ATTR_CURRENT_SCHEMA : user}, 1)
    except Exception as inst:
        raise _get_exception(inst)

    return Connection(conn)


class Connection(object):
    """This class object represents a connection between the database 
    and the application.

    """
    def __init__(self, conn_handler):
        """Constructor for Connection object. It takes IfxPy 
        connection handler as an argument. 

        """
        self.conn_handler = conn_handler

        # Used to identify close cursors for generating exceptions 
        # after the connection is closed.
        self._cursor_list = []
        self.__dbms_name = IfxPy.get_db_info(conn_handler, SQL_DBMS_NAME)
        self.__dbms_ver = IfxPy.get_db_info(conn_handler, SQL_DBMS_VER)
        self.FIX_RETURN_TYPE = 1 

    # This method is used to get the DBMS_NAME 
    def __get_dbms_name( self ):
        return self.__dbms_name

    # This attribute specifies the DBMS_NAME
    # It is a read only attribute. 
    dbms_name = property(__get_dbms_name, None, None, "")

    # This method is used to get the DBMS_ver 
    def __get_dbms_ver( self ):
        return self.__dbms_ver

    # This attribute specifies the DBMS_ver
    # It is a read only attribute. 
    dbms_ver = property(__get_dbms_ver, None, None, "")

    def close(self):
        """This method closes the Database connection associated with
        the Connection object.  It takes no arguments.

        """
        self.rollback()
        try:
            if self.conn_handler is None:
                raise ProgrammingError("Connection cannot be closed; "
                                     "connection is no longer active.")
            else:
                return_value = IfxPy.close(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        self.conn_handler = None
        for index in range(len(self._cursor_list)):
            if (self._cursor_list[index]() != None):
                tmp_cursor =  self._cursor_list[index]()
                tmp_cursor.conn_handler = None
                tmp_cursor.stmt_handler = None
                tmp_cursor._all_stmt_handlers = None
        self._cursor_list = []
        return return_value

    def commit(self):
        """This method commits the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = IfxPy.commit(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        return return_value

    def rollback(self):
        """This method rollbacks the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = IfxPy.rollback(self.conn_handler)
        except Exception as inst:
            raise _get_exception(inst)
        return return_value

    def cursor(self):
        """This method returns a Cursor object associated with the 
        Connection.  It takes no arguments.

        """
        if self.conn_handler is None:
            raise ProgrammingError("Cursor cannot be returned; "
                               "connection is no longer active.")
        cursor = Cursor(self.conn_handler, self)
        self._cursor_list.append(weakref.ref(cursor))
        return cursor

    # Sets connection attribute values
    def set_option(self, attr_dict):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        return IfxPy.set_option(self.conn_handler, attr_dict, 1)

    # Retrieves connection attributes values
    def get_option(self, attr_key):
        """Input: connection attribute key
           Return: current setting of the resource attribute requested
        """
        return IfxPy.get_option(self.conn_handler, attr_key, 1)

    # Sets FIX_RETURN_TYPE. Added for performance improvement
    def set_fix_return_type(self, is_on):
        try:
          if is_on:
            self.FIX_RETURN_TYPE = 1
          else:
            self.FIX_RETURN_TYPE = 0
        except Exception as inst:
          raise _get_exception(inst)
        return self.FIX_RETURN_TYPE

    # Sets connection AUTOCOMMIT attribute
    def set_autocommit(self, is_on):
        """Input: connection attribute: true if AUTOCOMMIT ON, false otherwise (i.e. OFF)
           Return: True on success or False on failure
        """
        try:
          if is_on:
            is_set = IfxPy.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_ON}, 1)
          else:
            is_set = IfxPy.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_OFF}, 1)
        except Exception as inst:
          raise _get_exception(inst)
        return is_set

    # # Sets connection attribute values
    def set_current_schema(self, schema_name):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        self.current_schema = schema_name
        try:
          # is_set = IfxPy.set_option(self.conn_handler, {SQL_ATTR_CURRENT_SCHEMA : schema_name}, 1)
          is_set = 'dummy'
        except Exception as inst:
          raise _get_exception(inst)
        return is_set

    # # Retrieves connection attributes values
    def get_current_schema(self):
        """Return: current setting of the schema attribute
        """
        try:
          # conn_schema = IfxPy.get_option(self.conn_handler, SQL_ATTR_CURRENT_SCHEMA, 1)
          conn_schema = 'dummy'
          if conn_schema is not None and conn_schema != '':
            self.current_schema = conn_schema
        except Exception as inst:
          raise _get_exception(inst)
        return self.current_schema


    # Retrieves the IBM Data Server version for a given Connection object
    def server_info(self):
        """Return: tuple (DBMS_NAME, DBMS_VER)
        """
        try:
          server_info = []
          server_info.append(self.dbms_name)
          server_info.append(self.dbms_ver)
        except Exception as inst:
          raise _get_exception(inst)
        return tuple(server_info)

    def set_case(self, str_value):
        return str_value.lower()

    # Retrieves the tables for a specified schema (and/or given table name)
    def tables(self, schema_name=None, table_name=None):
        """Input: connection - IfxPy.IFXConnection object
           Return: sequence of table metadata dicts for the specified schema
        """

        result = []
        if schema_name is not None:
            schema_name = self.set_case(schema_name)
        if table_name is not None:
            table_name = self.set_case(table_name)

        try:
          stmt = IfxPy.tables(self.conn_handler, None, schema_name, table_name)
          row = IfxPy.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1
              row = IfxPy.fetch_assoc(stmt)
          IfxPy.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result

    # Retrieves metadata pertaining to index for specified schema (and/or table name)
    def indexes(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - IfxPy.IFXConnection object
           Return: sequence of index metadata dicts for the specified table
        Example:
           Index metadata retrieved from schema 'PYTHONIC.TEST_TABLE' table
           {
           'TABLE_SCHEM':       'PYTHONIC',              'TABLE_CAT':          None, 
           'TABLE_NAME':        'ENGINE_USERS',          'PAGES':              None, 
           'COLUMN_NAME':       'USER_ID'                'FILTER_CONDITION':   None, 
           'INDEX_NAME':        'SQL071201150750170',    'CARDINALITY':        None,
           'ORDINAL_POSITION':   1,                      'INDEX_QUALIFIER':   'SYSIBM', 
           'TYPE':               3, 
           'NON_UNIQUE':         0, 
           'ASC_OR_DESC':       'A'
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case(schema_name)
        if table_name is not None:
            table_name = self.set_case(table_name)

        try:
          stmt = IfxPy.statistics(self.conn_handler, None, schema_name, table_name, unique)
          row = IfxPy.fetch_assoc(stmt)
          i = 0
          while (row):
              if row['TYPE'] == SQL_INDEX_OTHER:
                  result.append( row )
              i += 1
              row = IfxPy.fetch_assoc(stmt)
          IfxPy.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result

    # Retrieves metadata pertaining to primary keys for specified schema (and/or table name)
    def primary_keys(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - IfxPy.IFXConnection object
           Return: sequence of PK metadata dicts for the specified table
        Example:
           PK metadata retrieved from 'PYTHONIC.ORDERS' table
           {  
           'TABLE_SCHEM':  'PYTHONIC',                 'TABLE_CAT': None, 
           'TABLE_NAME':   'ORDERS', 
           'COLUMN_NAME':  'ORDER_ID'
           'PK_NAME':      'SQL071128122038680', 
           'KEY_SEQ':       1
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case(schema_name)
        if table_name is not None:
            table_name = self.set_case(table_name)

        try:
          stmt = IfxPy.primary_keys(self.conn_handler, None, schema_name, table_name)
          row = IfxPy.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1
              row = IfxPy.fetch_assoc(stmt)
          IfxPy.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result

    # Retrieves metadata pertaining to foreign keys for specified schema (and/or table name)
    def foreign_keys(self, unique=True, schema_name=None, table_name=None):
        """Input: connection - IfxPy.IFXConnection object
           Return: sequence of FK metadata dicts for the specified table
        Example:
           FK metadata retrieved from 'PYTHONIC.ENGINE_EMAIL_ADDRESSES' table
           {
           'PKTABLE_SCHEM': 'PYTHONIC',                 'PKTABLE_CAT':    None, 
           'PKTABLE_NAME':  'ENGINE_USERS',             'FKTABLE_CAT':    None,
           'PKCOLUMN_NAME': 'USER_ID',                  'UPDATE_RULE':    3,
           'PK_NAME':       'SQL071205090958680',       'DELETE_RULE':    3
           'KEY_SEQ':        1,                         'DEFERRABILITY':  7, 
           'FK_NAME':       'SQL071205091000160', 
           'FKCOLUMN_NAME': 'REMOTE_USER_ID', 
           'FKTABLE_NAME':  'ENGINE_EMAIL_ADDRESSES', 
           'FKTABLE_SCHEM': 'PYTHONIC' 
           }
        """
        result = []
        if schema_name is not None:
            schema_name = self.set_case(schema_name)
        if table_name is not None:
            table_name = self.set_case(table_name)

        try:
          stmt = IfxPy.foreign_keys(self.conn_handler, None, None, None, None, schema_name, table_name)
          row = IfxPy.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1
              row = IfxPy.fetch_assoc(stmt)
          IfxPy.free_result(stmt)
        except Exception as inst:
          raise _get_exception(inst)

        return result

    # Retrieves the columns for a specified schema (and/or table name and column name)
    def columns(self, schema_name=None, table_name=None, column_names=None):
        """Input: connection - IfxPy.IFXConnection object
           Return: sequence of column metadata dicts for the specified schema
        Example:
           Column metadata retrieved from schema 'PYTHONIC.FOO' table, column 'A'
           {
           'TABLE_NAME':        'FOO',        'NULLABLE':           1, 
           'ORDINAL_POSITION':   2L,          'REMARKS':            None, 
           'COLUMN_NAME':       'A',          'BUFFER_LENGTH':      30L, 
           'TYPE_NAME':         'VARCHAR',    'SQL_DATETIME_SUB':   None, 
           'COLUMN_DEF':         None,        'DATA_TYPE':          12, 
           'IS_NULLABLE':       'YES',        'SQL_DATA_TYPE':      12, 
           'COLUMN_SIZE':        30L,         'TABLE_CAT':          None, 
           'CHAR_OCTET_LENGTH':  30L,         'TABLE_SCHEM':       'PYTHONIC',
           'NUM_PREC_RADIX':     None,
           'DECIMAL_DIGITS':     None
           }
        """
        result = []
        if schema_name is not None:
          schema_name = self.set_case(schema_name)
        if table_name is not None:
          table_name = self.set_case(table_name)

        try:
          stmt = IfxPy.columns(self.conn_handler, None, schema_name, table_name)
          row = IfxPy.fetch_assoc(stmt)
          i = 0
          while (row):
            result.append( row )
            i += 1
            row = IfxPy.fetch_assoc(stmt)
          IfxPy.free_result(stmt)

          col_names_lower = []
          if column_names is not None:
            for name in column_names:
              col_names_lower.append(name.lower())
            include_columns = []
            if column_names and column_names != '':
              for column in result:
                if column['COLUMN_NAME'].lower() in col_names_lower:
                  column['COLUMN_NAME'] = column['COLUMN_NAME'].lower()
                  include_columns.append(column)
              result = include_columns
        except Exception as inst:
          raise _get_exception(inst)

        return result


# Defines a cursor for the driver connection
class Cursor(object):
    """This class represents a cursor of the connection.  It can be
    used to process an SQL statement.
    """

    # This method is used to get the description attribute.
    def __get_description(self):
        """ If this method has already been called, after executing a select statement,
            return the stored information in the self.__description.
        """
        if self.__description is not None:
            return self.__description 

        if self.stmt_handler is None:
            return None
        self.__description = []

        try:
            num_columns = IfxPy.num_fields(self.stmt_handler)
            """ If the execute statement did not produce a result set return None.
            """
            if num_columns == False:
                self.__description = None
                return None
            for column_index in range(num_columns):
                column_desc = []
                column_desc.append(IfxPy.field_name(self.stmt_handler,
                                                          column_index))
                type = IfxPy.field_type(self.stmt_handler, column_index)
                type = type.upper()
                if STRING == type:
                    column_desc.append(STRING)
                elif TEXT == type:
                    column_desc.append(TEXT)
#                elif XML == type:
#                    column_desc.append(XML)
                elif BINARY == type:
                    column_desc.append(BINARY)
                elif NUMBER == type:
                    column_desc.append(NUMBER)
                elif BIGINT == type:
                    column_desc.append(BIGINT)
                elif FLOAT == type:
                    column_desc.append(FLOAT)
                elif DECIMAL == type:
                    column_desc.append(DECIMAL)
                elif DATE == type:
                    column_desc.append(DATE)
                elif TIME == type:
                    column_desc.append(TIME)
                elif DATETIME == type:
                    column_desc.append(DATETIME)
                elif ROWID == type:
                    column_desc.append(ROWID)

                column_desc.append(IfxPy.field_display_size(
                                             self.stmt_handler, column_index))

                column_desc.append(IfxPy.field_display_size(
                                             self.stmt_handler, column_index))

                column_desc.append(IfxPy.field_precision(
                                             self.stmt_handler, column_index))

                column_desc.append(IfxPy.field_scale(self.stmt_handler,
                                                                column_index))

                column_desc.append(IfxPy.field_nullable(
                                             self.stmt_handler, column_index))

                self.__description.append(column_desc)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]

        return self.__description

    # This attribute provides the metadata information of the columns
    # in the result set produced by the last execute function.  It is
    # a read only attribute.
    description = property(fget = __get_description)

    # This method is used to get the rowcount attribute.
    def __get_rowcount( self ):
        return self.__rowcount

    def __iter__( self ):
        return self

    def __next__( self ):
        row = self.fetchone()
        if row == None:
            raise StopIteration
        return row

    # This attribute specifies the number of rows the last executeXXX()
    # produced or affected.  It is a read only attribute.
    rowcount = property(__get_rowcount, None, None, "")

    # This method is used to get the Connection object
    def __get_connection( self ):
        return self.__connection

    # This attribute specifies the connection object.
    # It is a read only attribute.
    connection = property(__get_connection, None, None, "")

    def __init__(self, conn_handler, conn_object=None):
        """Constructor for Cursor object. It takes IfxPy connection
        handler as an argument.
        """

        # This attribute is used to determine the fetch size for fetchmany
        # operation. It is a read/write attribute
        self.arraysize = 1
        self.__rowcount = -1
        self._result_set_produced = False
        self.__description = None
        self.conn_handler = conn_handler
        self.stmt_handler = None
        self._is_scrollable_cursor = False
        self.__connection = conn_object
        self.messages = []
        self.FIX_RETURN_TYPE = conn_object.FIX_RETURN_TYPE

    # This method closes the statemente associated with the cursor object.
    # It takes no argument.
    def close(self):
        """This method closes the cursor object.  After this method is 
        called the cursor object is no longer usable.  It takes no
        arguments.

        """
        messages = []
        if self.conn_handler is None:
            self.messages.append(ProgrammingError("Cursor cannot be closed; connection is no longer active."))
            raise self.messages[len(self.messages) - 1]
        try:
            return_value = IfxPy.free_stmt(self.stmt_handler)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]
        self.stmt_handler = None
        self.conn_handler = None
        self._all_stmt_handlers = None
        if self.__connection is not None:
            try:
                self.__connection._cursor_list.remove(weakref.ref(self))
            except:
                pass
        return return_value

    # helper for calling procedure
    def _callproc_helper(self, procname, parameters=None):
        if parameters is not None:
            buff = []
            CONVERT_STR = (buffer)
            # Convert date/time and binary objects to string for 
            # inserting into the database. 
            for param in parameters:
                if isinstance(param, CONVERT_STR):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)

            try:
                result = IfxPy.callproc(self.conn_handler, procname,parameters)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
        else:
            try:
                result = IfxPy.callproc(self.conn_handler, procname)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
        return result


    def callproc(self, procname, parameters=None):
        """This method can be used to execute a stored procedure.  
        It takes the name of the stored procedure and the parameters to
        the stored procedure as arguments. 

        """
        self.messages = []
        if not isinstance(procname, str):
            self.messages.append(InterfaceError("callproc expects the first argument to be of type String or Unicode."))
            raise self.messages[len(self.messages) - 1]
        if parameters is not None:
            if not isinstance(parameters, (list, tuple)):
                self.messages.append(InterfaceError("callproc expects the second argument to be of type list or tuple."))
                raise self.messages[len(self.messages) - 1]
        result = self._callproc_helper(procname, parameters)
        return_value = None
        self.__description = None
        self._all_stmt_handlers = []
        if isinstance(result, tuple):
            self.stmt_handler = result[0]
            return_value = result[1:]
        else:
            self.stmt_handler = result
        self._result_set_produced = True
        return return_value

    # Helper for preparing an SQL statement.
    def _prepare_helper(self, operation, parameters=None):
        try:
            IfxPy.free_stmt(self.stmt_handler)
        except:
            pass

        try:
            self.stmt_handler = IfxPy.prepare(self.conn_handler, operation)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]

    # Helper for preparing an SQL statement.
    def _set_cursor_helper(self):
        if (IfxPy.get_option(self.stmt_handler, IfxPy.SQL_ATTR_CURSOR_TYPE, 0) != IfxPy.SQL_CURSOR_FORWARD_ONLY):
            self._is_scrollable_cursor = True
        else:
            self._is_scrollable_cursor = False
        self._result_set_produced = False
        try:
            num_columns = IfxPy.num_fields(self.stmt_handler)
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]
        if not num_columns:
            return True
        self._result_set_produced = True

        return True

    # Helper for executing an SQL statement.
    def _execute_helper(self, parameters=None):
        if parameters is not None:
            buff = []
            CONVERT_STR = (buffer)
            # Convert date/time and binary objects to string for
            # inserting into the database.
            for param in parameters:
                if isinstance(param, CONVERT_STR):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)
            try:
                return_value = IfxPy.execute(self.stmt_handler, parameters)
                if not return_value:
                    if IfxPy.conn_errormsg() is not None:
                        self.messages.append(Error(str(IfxPy.conn_errormsg())))
                        raise self.messages[len(self.messages) - 1]
                    if IfxPy.stmt_errormsg() is not None:
                        self.messages.append(Error(str(IfxPy.stmt_errormsg())))
                        raise self.messages[len(self.messages) - 1]
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
        else:
            try:
                return_value = IfxPy.execute(self.stmt_handler)
                if not return_value:
                    if IfxPy.conn_errormsg() is not None:
                        self.messages.append(Error(str(IfxPy.conn_errormsg())))
                        raise self.messages[len(self.messages) - 1]
                    if IfxPy.stmt_errormsg() is not None:
                        self.messages.append(Error(str(IfxPy.stmt_errormsg())))
                        raise self.messages[len(self.messages) - 1]
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
        return return_value

    # This method is used to set the rowcount after executing an SQL statement.
    def _set_rowcount(self):
        self.__rowcount = -1
        if not self._result_set_produced:
            try:
                counter = IfxPy.num_rows(self.stmt_handler)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
            self.__rowcount = counter
        elif self._is_scrollable_cursor:
            try:
                counter = IfxPy.get_num_result(self.stmt_handler)
            except Exception as inst:
                self.messages.append(_get_exception(inst))
                raise self.messages[len(self.messages) - 1]
            if counter >= 0:
                self.__rowcount = counter
        return True

    # Retrieves the last generated identity value from the Informix catalog
    def _get_last_identity_val(self):
        """
        The result of the IDENTITY_VAL_LOCAL function is not affected by the following:
         - A single row INSERT statement with a VALUES clause for a table without an
        identity column
         - A multiple row INSERT statement with a VALUES clause
         - An INSERT statement with a fullselect

        """
        operation = 'SELECT IDENTITY_VAL_LOCAL() FROM SYSIBM.SYSDUMMY1'
        try:
            stmt_handler = IfxPy.prepare(self.conn_handler, operation)
            if IfxPy.execute(stmt_handler):
                row = IfxPy.fetch_tuple(stmt_handler)
                if row[0] is not None:
                  identity_val = int(row[0])
                else:
                  identity_val = None
            else:
                if IfxPy.conn_errormsg() is not None:
                    self.messages.append(Error(str(IfxPy.conn_errormsg())))
                    raise self.messages[len(self.messages) - 1]
                if IfxPy.stmt_errormsg() is not None:
                    self.messages.append(Error(str(IfxPy.stmt_errormsg())))
                    raise self.messages[len(self.messages) - 1]
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]
        return identity_val
    last_identity_val = property(_get_last_identity_val, None, None, "")

    def execute(self, operation, parameters=None):
        """
        This method can be used to prepare and execute an SQL 
        statement.  It takes the SQL statement(operation) and a 
        sequence of values to substitute for the parameter markers in  
        the SQL statement as arguments.
        """
        self.messages = []
        if not isinstance(operation, str):
            self.messages.append(InterfaceError("execute expects the first argument [%s] to be of type String or Unicode." % operation ))
            raise self.messages[len(self.messages) - 1]
        if parameters is not None:
            if not isinstance(parameters, (list, tuple, dict)):
                self.messages.append(InterfaceError("execute parameters argument should be sequence."))
                raise self.messages[len(self.messages) - 1]
        self.__description = None
        self._all_stmt_handlers = []
        self._prepare_helper(operation)
        self._set_cursor_helper()
        self._execute_helper(parameters)
        return self._set_rowcount()

    def executemany(self, operation, seq_parameters):
        """
        This method can be used to prepare, and then execute an SQL 
        statement many times.  It takes the SQL statement(operation) 
        and sequence of sequence of values to substitute for the 
        parameter markers in the SQL statement as its argument.
        """
        self.messages = []
        if not isinstance(operation, str):
            self.messages.append(InterfaceError("executemany expects the first argument to be of type String or Unicode."))
            raise self.messages[len(self.messages) - 1]
        if seq_parameters is None:
            self.messages.append(InterfaceError("executemany expects a not None seq_parameters value"))
            raise self.messages[len(self.messages) - 1]

        if not isinstance(seq_parameters, (list, tuple)):
            self.messages.append(InterfaceError("executemany expects the second argument to be of type list or tuple of sequence."))
            raise self.messages[len(self.messages) - 1]

        CONVERT_STR = (buffer)
        # Convert date/time and binary objects to string for
        # inserting into the database.
        buff = []
        seq_buff = []
        for index in range(len(seq_parameters)):
            buff = []
            for param in seq_parameters[index]:
                if isinstance(param, CONVERT_STR):
                    param = str(param)
                buff.append(param)
            seq_buff.append(tuple(buff))
        seq_parameters = tuple(seq_buff)
        self.__description = None
        self._all_stmt_handlers = []
        self.__rowcount = -1
        self._prepare_helper(operation)
        try:
            autocommit = IfxPy.autocommit(self.conn_handler)
            if autocommit !=  0:
                IfxPy.autocommit(self.conn_handler, 0)
            self.__rowcount = IfxPy.execute_many(self.stmt_handler, seq_parameters)
            if autocommit != 0:
                IfxPy.commit(self.conn_handler)
                IfxPy.autocommit(self.conn_handler, autocommit)
            if self.__rowcount == -1:
                if IfxPy.conn_errormsg() is not None:
                    self.messages.append(Error(str(IfxPy.conn_errormsg())))
                    raise self.messages[len(self.messages) - 1]
                if IfxPy.stmt_errormsg() is not None:
                    self.messages.append(Error(str(IfxPy.stmt_errormsg())))
                    raise self.messages[len(self.messages) - 1]
        except Exception as inst:
            self._set_rowcount()
            self.messages.append(Error(inst))
            raise self.messages[len(self.messages) - 1]
        return True

    def _fetch_helper(self, fetch_size=-1):
        """
        This method is a helper function for fetching fetch_size number of
        rows, after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.
        If this is not provided it fetches all the remaining rows.
        """
        if self.stmt_handler is None:
            self.messages.append(ProgrammingError("Please execute an SQL statement in order to get a row from result set."))
            raise self.messages[len(self.messages) - 1]
        if self._result_set_produced == False:
            self.messages.append(ProgrammingError("The last call to execute did not produce any result set."))
            raise  self.messages[len(self.messages) - 1]
        row_list = []
        rows_fetched = 0
        while (fetch_size == -1) or (fetch_size != -1 and rows_fetched < fetch_size):
            try:
                row = IfxPy.fetch_tuple(self.stmt_handler)
            except Exception as inst:
                if IfxPy.stmt_errormsg() is not None:
                    self.messages.append(Error(str(IfxPy.stmt_errormsg())))
                else:
                    self.messages.append(_get_exception(inst))
                if len(row_list) == 0:
                    raise self.messages[len(self.messages) - 1]
                else:
                    return row_list

            if row != False:
                if self.FIX_RETURN_TYPE == 1:
                    row_list.append(self._fix_return_data_type(row))
                else:
                    row_list.append(row)
            else:
                return row_list
            rows_fetched = rows_fetched + 1
        return row_list

    def fetchone(self):
        """This method fetches one row from the database, after 
        executing an SQL statement which produces a result set.

        """
        row_list = self._fetch_helper(1)
        if len(row_list) == 0:
            return None
        else:
            return row_list[0]

    def fetchmany(self, size=0):
        """This method fetches size number of rows from the database,
        after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.  If this 
        is not provided it fetches self.arraysize number of rows. 
        """
        if not isinstance(size, int):
            self.messages.append(InterfaceError( "fetchmany expects argument type int or long."))
            raise self.messages[len(self.messages) - 1]
        if size == 0:
            size = self.arraysize
        if size < -1:
            self.messages.append(ProgrammingError("fetchmany argument size expected to be positive."))
            raise self.messages[len(self.messages) - 1]

        return self._fetch_helper(size)

    def fetchall(self):
        """This method fetches all remaining rows from the database,
        after executing an SQL statement which produces a result set.
        """
        return self._fetch_helper()

    def nextset(self):
        """This method can be used to get the next result set after 
        executing a stored procedure, which produces multiple result sets.
        """
        self.messages = []
        if self.stmt_handler is None:
            self.messages.append(ProgrammingError("Please execute an SQL statement in order to get result sets."))
            raise self.messages[len(self.messages) - 1]
        if self._result_set_produced == False:
            self.messages.append(ProgrammingError("The last call to execute did not produce any result set."))
            raise self.messages[len(self.messages) - 1]
        try:
            # Store all the stmt handler that were created.
            # The handler was the one created by the execute method.
            # It should be used to get next result set.
            self.__description = None
            self._all_stmt_handlers.append(self.stmt_handler)
            self.stmt_handler = IfxPy.next_result(self._all_stmt_handlers[0])
        except Exception as inst:
            self.messages.append(_get_exception(inst))
            raise self.messages[len(self.messages) - 1]

        if self.stmt_handler == False:
            self.stmt_handler = None
        if self.stmt_handler == None:
            return None
        return True

    def setinputsizes(self, sizes):
        """This method currently does nothing."""
        pass

    def setoutputsize(self, size, column=-1):
        """This method currently does nothing."""
        pass

    # This method is used to convert a string representing decimal
    # and binary data in a row tuple fetched from the database
    # to decimal and binary objects, for returning it to the user.
    def _fix_return_data_type(self, row):
        row_list = None
        for index in range(len(row)):
            if row[index] is not None:
                type = IfxPy.field_type(self.stmt_handler, index)
                type = type.upper()

                try:
                    if type == 'BLOB':
                        if row_list is None:
                            row_list = list(row)
                        row_list[index] = buffer(row[index])

                    elif type == 'DECIMAL':
                        if row_list is None:
                            row_list = list(row)
                        row_list[index] = decimal.Decimal(str(row[index]).replace(",", "."))

                except Exception as inst:
                    self.messages.append(DataError("Data type format error: "+ str(inst)))
                    raise self.messages[len(self.messages) - 1]
        if row_list is None:
            return row
        else:
            return tuple(row_list)


#################################################
# We can use this for SPEED TEST between Py and C
# Find the number of prime numbers between X and Y
# The equivalent C function is SpeedTestWithCPrimeCount
def SpeedTestWithPyPrimeCount(x, y):
    i = 0
    j = 0
    VRange = 0.0
    isPrime = 0
    PrimeCount = 0

    if x < 2:
        x = 2

    y += 1
    i = x
    while ( i < y):
        isPrime = 1
        VRange = i / 2 # This Validation Range is good enough

        j = 2
        VRange += 1
        while ( j < VRange ):
            if ( i%j == 0):
                j += 1
                isPrime = 0
                break
            j += 1

        if (isPrime):
            #print( ' [{:d}] '.format(i))
            PrimeCount += 1

        i += 1

    return PrimeCount