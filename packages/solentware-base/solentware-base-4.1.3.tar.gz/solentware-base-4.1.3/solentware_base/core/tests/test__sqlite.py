# test__sqlite.py
# Copyright 2019 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""_sqlite _database tests"""

import unittest
import os
try:
    import sqlite3
except ImportError: # Not ModuleNotFoundError for Pythons earlier than 3.6
    sqlite3 = None
try:
    import apsw
except ImportError: # Not ModuleNotFoundError for Pythons earlier than 3.6
    apsw = None

from .. import _sqlite
from .. import filespec
from .. import recordset
from ..segmentsize import SegmentSize
from ..wherevalues import ValuesClause


class _SQLite(unittest.TestCase):
    # The sets of tests are run inside a loop for sqlite3 and apsw, and some
    # tests change SegmentSize.db_segment_size_bytes, so reset it to the
    # initial value in tearDown().

    def setUp(self):
        self._ssb = SegmentSize.db_segment_size_bytes
        class _D(_sqlite.Database):
            pass
        self._D = _D

    def tearDown(self):
        self.database = None
        self._D = None
        SegmentSize.db_segment_size_bytes = self._ssb


class Database___init__(_SQLite):

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "__init__\(\) takes from 2 to 5 positional arguments ",
                "but 6 were given",
                )),
            self._D,
            *(None, None, None, None, None),
            )

    def test_02(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "type object argument after \*\* must be a mapping, ",
                "not NoneType",
                )),
            self._D,
            *(None,),
            )
        self.assertIsInstance(self._D({}), self._D)
        self.assertIsInstance(self._D(filespec.FileSpec()), self._D)

    def test_03(self):
        self.assertRaisesRegex(
            _sqlite.DatabaseError,
            "".join((
                "Database folder name {} is not valid",
                )),
            self._D,
            *({},),
            **dict(folder={}),
            )

    def test_04(self):
        database = self._D({}, folder='a')
        self.assertIsInstance(database, self._D)
        self.assertEqual(os.path.basename(database.home_directory), 'a')
        self.assertEqual(os.path.basename(database.database_file), 'a')
        self.assertEqual(os.path.basename(
            os.path.dirname(database.database_file)), 'a')
        self.assertEqual(database.specification, {})
        self.assertEqual(database.segment_size_bytes, 4000)
        self.assertEqual(database.dbenv, None)
        self.assertEqual(database.table, {})
        self.assertEqual(database.index, {})
        self.assertEqual(database.segment_table, {})
        self.assertEqual(database.ebm_control, {})
        self.assertEqual(database.ebm_segment_count, {})
        self.assertEqual(SegmentSize.db_segment_size_bytes, 4096)
        database.set_segment_size()
        self.assertEqual(SegmentSize.db_segment_size_bytes, 4000)

    def test_05(self):
        database = self._D({})
        self.assertEqual(database.home_directory, None)
        self.assertEqual(database.database_file, None)

    # This combination of folder and segment_size_bytes arguments is used for
    # unittests, except for one to see a non-memory database with a realistic
    # segment size.
    def test_06(self):
        ssb = self._ssb
        database = self._D({}, segment_size_bytes=None)
        self.assertEqual(database.segment_size_bytes, None)
        database.set_segment_size()
        self.assertEqual(SegmentSize.db_segment_size_bytes, 16)
        self._ssb = ssb


# Transaction methods do not raise exceptions if called when no database open
# but do nothing.
class Database_transaction_methods(_SQLite):

    def setUp(self):
        super().setUp()
        self.database = self._D({})

    def test_01_start_transaction(self):
        self.assertEqual(self.database.dbenv, None)
        self.database.start_transaction()

    def test_02_backout(self):
        self.assertEqual(self.database.dbenv, None)
        self.database.backout()

    def test_03_commit(self):
        self.assertEqual(self.database.dbenv, None)
        self.database.commit()

    def test_04(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "start_transaction\(\) takes 1 positional argument ",
                "but 2 were given",
                )),
            self.database.start_transaction,
            *(None,),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "backout\(\) takes 1 positional argument ",
                "but 2 were given",
                )),
            self.database.backout,
            *(None,),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "commit\(\) takes 1 positional argument ",
                "but 2 were given",
                )),
            self.database.commit,
            *(None,),
            )


# Methods which do not require database to be open.
class DatabaseInstance(_SQLite):

    def setUp(self):
        super().setUp()
        self.database = self._D({})

    def test_01_validate_segment_size_bytes(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "_validate_segment_size_bytes\(\) missing 1 required ",
                "positional argument: 'segment_size_bytes'",
                )),
            self.database._validate_segment_size_bytes,
            )
        self.assertRaisesRegex(
            _sqlite.DatabaseError,
            "".join((
                "Database segment size must be an int",
                )),
            self.database._validate_segment_size_bytes,
            *('a',),
            )
        self.assertRaisesRegex(
            _sqlite.DatabaseError,
            "".join((
                "Database segment size must be more than 0",
                )),
            self.database._validate_segment_size_bytes,
            *(0,),
            )
        self.assertEqual(self.database._validate_segment_size_bytes(None), None)
        self.assertEqual(self.database._validate_segment_size_bytes(1), None)

    def test_02_encode_record_number(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "encode_record_number\(\) missing 1 required ",
                "positional argument: 'key'",
                )),
            self.database.encode_record_number,
            )
        self.assertEqual(self.database.encode_record_number(1), '1')

    def test_03_decode_record_number(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "decode_record_number\(\) missing 1 required ",
                "positional argument: 'skey'",
                )),
            self.database.decode_record_number,
            )
        self.assertEqual(self.database.decode_record_number('1'), 1)

    def test_04_encode_record_selector(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "encode_record_selector\(\) missing 1 required ",
                "positional argument: 'key'",
                )),
            self.database.encode_record_selector,
            )
        self.assertEqual(self.database.encode_record_selector('a'), 'a')

    def test_05_make_recordset(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_nil\(\) takes from 2 to 3 positional arguments ",
                "but 4 were given",
                )),
            self.database.recordlist_nil,
            *(None, None, None),
            )
        self.assertIsInstance(self.database.recordlist_nil('a'),
                              recordset.RecordList)


# Memory databases are used for these tests.
class Database_open_database(_SQLite):

    def test_01(self):
        self.database = self._D({})
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "open_database\(\) takes from 2 to 3 positional arguments ",
                "but 4 were given",
                )),
            self.database.open_database,
            *(None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "close_database\(\) takes 1 positional argument ",
                "but 2 were given",
                )),
            self.database.close_database,
            *(None,),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "close_database_contexts\(\) takes from 1 to 2 positional ",
                "arguments but 3 were given",
                )),
            self.database.close_database_contexts,
            *(None, None),
            )

    def test_02(self):
        self.database = self._D({})
        self.database.open_database(dbe_module)
        self.assertEqual(SegmentSize.db_segment_size_bytes, 4000)
        self.assertEqual(self.database.home_directory, None)
        self.assertEqual(self.database.database_file, None)
        self.assertIsInstance(self.database.dbenv, dbe_module.Connection)

    def test_03(self):
        self.database = self._D({}, segment_size_bytes=None)
        self.database.open_database(dbe_module)
        self.assertEqual(SegmentSize.db_segment_size_bytes, 16)
        self.assertEqual(self.database.home_directory, None)
        self.assertEqual(self.database.database_file, None)
        self.assertIsInstance(self.database.dbenv, dbe_module.Connection)

    def test_04_close_database(self):
        self.database = self._D({}, segment_size_bytes=None)
        self.database.open_database(dbe_module)
        self.database.close_database()
        self.assertEqual(self.database.dbenv, None)
        self.database.close_database()
        self.assertEqual(self.database.dbenv, None)

    def test_05_close_database_contexts(self):
        self.database = self._D({}, segment_size_bytes=None)
        self.database.open_database(dbe_module)
        self.database.close_database_contexts()
        self.assertEqual(self.database.dbenv, None)
        self.database.close_database_contexts()
        self.assertEqual(self.database.dbenv, None)

    def test_06(self):
        self.database = self._D({'file1': {'field1'}})
        self.database.open_database(dbe_module)
        self.check_specification()

    def test_07(self):
        self.database = self._D(filespec.FileSpec(**{'file1': {'field1'}}))
        self.database.open_database(dbe_module)
        self.check_specification()

    def test_08(self):
        self.database = self._D(
            filespec.FileSpec(**{'file1': {'field1'}, 'file2': {'field2'}}))
        self.database.open_database(dbe_module, files={'file1'})
        self.check_specification()

    def test_09(self):
        self.database = self._D(
            filespec.FileSpec(**{'file1': {'field1'}, 'file2': ()}))
        self.database.open_database(dbe_module)
        self.assertEqual(
            self.database.table,
            {'file1': ['file1'],
             '___control': '___control',
             'file1_field1': ['file1_field1'],
             'file2': ['file2'],
             })
        self.assertEqual(
            self.database.index, {'file1_field1': ['ixfile1_field1']})

        self.assertEqual(
            self.database.segment_table,
            {'file1': 'file1__segment', 'file2': 'file2__segment'})
        self.assertEqual(
            self.database.ebm_control['file1']._file, 'file1')
        self.assertEqual(
            self.database.ebm_control['file1'].ebm_table, 'file1__ebm')
        self.assertEqual(
            self.database.ebm_control['file2']._file, 'file2')
        self.assertEqual(
            self.database.ebm_control['file2'].ebm_table, 'file2__ebm')
        self.assertEqual(self.database.ebm_segment_count, {})
        for v in self.database.ebm_control.values():
            self.assertIsInstance(v, _sqlite.ExistenceBitmapControl)

    # Comment in _sqlite.py suggests this method is not needed.
    def test_12_is_database_file_active(self):
        self.database = self._D(
            filespec.FileSpec(**{'file1': {'field1'}, 'file2': ()}))
        d = self.database
        self.assertEqual(d.is_database_file_active('file1'), False)
        d.open_database(dbe_module)
        self.assertEqual(d.is_database_file_active('file1'), True)
        
    def check_specification(self):
        self.assertEqual(
            self.database.table,
            {'file1': ['file1'],
             '___control': '___control',
             'file1_field1': ['file1_field1'],
             })
        self.assertEqual(
            self.database.index, {'file1_field1': ['ixfile1_field1']})
        self.assertEqual(
            self.database.segment_table, {'file1': 'file1__segment'})
        self.assertEqual(self.database.ebm_control['file1']._file, 'file1')
        self.assertEqual(self.database.ebm_control['file1'].ebm_table,
                         'file1__ebm')
        self.assertEqual(self.database.ebm_segment_count, {})
        for v in self.database.ebm_control.values():
            self.assertIsInstance(v, _sqlite.ExistenceBitmapControl)


# Memory databases are used for these tests.
# This one has to look like a real application (almost).
# Do not need to catch the self.__class__.SegmentSizeError exception in
# _ED.open_database() method.
class Database_do_database_task(unittest.TestCase):
    # The sets of tests are run inside a loop for sqlite3 and apsw, and some
    # tests in this set change SegmentSize.db_segment_size_bytes, so reset it
    # to the initial value in tearDown().
    # _SQLite does this, but Database_do_database_task is not based on it.

    def setUp(self):
        self._ssb = SegmentSize.db_segment_size_bytes
        class _ED(_sqlite.Database):
            def open_database(self, **k):
                super().open_database(dbe_module, **k)
        class _AD(_ED):
            def __init__(self, folder, **k):
                super().__init__({}, folder, **k)
        self._AD = _AD

    def tearDown(self):
        self.database = None
        self._AD = None
        SegmentSize.db_segment_size_bytes = self._ssb

    def test_01_do_database_task(self):
        def m(*a, **k):
            pass
        self.database = self._AD(None)
        d = self.database
        d.open_database()
        self.assertEqual(d.do_database_task(m), None)


# Memory databases are used for these tests.
# Use the 'testing only' segment size for convenience of setup and eyeballing.
class _SQLiteOpen(_SQLite):

    def setUp(self):
        super().setUp()
        self.database = self._D(
            filespec.FileSpec(**{'file1': {'field1'}}),
            segment_size_bytes=None)
        self.database.open_database(dbe_module)

    def tearDown(self):
        self.database.close_database()
        super().tearDown()


class DatabaseTransactions(_SQLiteOpen):

    # apsw exception is apsw.SQLError
    # sqlite3 exception is sqlite3.OperationalError
    def test_01(self):
        self.database.start_transaction()
        self.assertRaisesRegex(
            Exception,
            "cannot start a transaction within a transaction",
            self.database.start_transaction,
            )

    def test_02(self):
        self.database.start_transaction()
        self.database.backout()

    def test_03(self):
        self.database.start_transaction()
        self.database.commit()

    # apsw exception is apsw.SQLError
    # sqlite3 exception is sqlite3.OperationalError
    def test_04(self):
        self.assertRaisesRegex(
            Exception,
            "cannot rollback - no transaction is active",
            self.database.backout,
            )

    # apsw exception is apsw.SQLError
    # sqlite3 exception is sqlite3.OperationalError
    def test_05(self):
        self.assertRaisesRegex(
            Exception,
            "cannot commit - no transaction is active",
            self.database.commit,
            )


class Database_put_replace_delete(_SQLiteOpen):

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "put\(\) missing 3 required positional arguments: ",
                "'file', 'key', and 'value'",
                )),
            self.database.put,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "replace\(\) missing 4 required positional arguments: ",
                "'file', 'key', 'oldvalue', and 'newvalue'",
                )),
            self.database.replace,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "delete\(\) missing 3 required positional arguments: ",
                "'file', 'key', and 'value'",
                )),
            self.database.delete,
            )

    def test_02_put(self):
        recno = self.database.put('file1', None, 'new value')
        self.assertEqual(recno, 1)

    def test_03_put(self):
        self.assertEqual(self.database.put('file1', 2, 'new value'), None)
        recno = self.database.put('file1', None, 'new value')
        self.assertEqual(recno, 3)

    def test_04_put(self):
        recno = self.database.put('file1', None, 'new value')
        self.assertEqual(recno, 1)
        self.assertEqual(self.database.put('file1', 1, 'renew value'), None)
        recno = self.database.put('file1', None, 'other value')
        self.assertEqual(recno, 2)

    def test_05_replace(self):
        self.assertEqual(self.database.replace(
            'file1', 1, 'new value', 'renew value'), None)

    def test_06_delete(self):
        self.assertEqual(self.database.delete(
            'file1', 1, 'new value'), None)


class Database_methods(_SQLiteOpen):

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_primary_record\(\) missing 2 required positional ",
                "arguments: 'file' and 'key'",
                )),
            self.database.get_primary_record,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "remove_record_from_ebm\(\) missing 2 required ",
                "positional arguments: 'file' and 'deletekey'",
                )),
            self.database.remove_record_from_ebm,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "add_record_to_ebm\(\) missing 2 required ",
                "positional arguments: 'file' and 'putkey'",
                )),
            self.database.add_record_to_ebm,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_high_record\(\) missing 1 required ",
                "positional argument: 'file'",
                )),
            self.database.get_high_record,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_segment_records\(\) missing 2 required ",
                "positional arguments: 'rownumber' and 'file'",
                )),
            self.database.get_segment_records,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "set_segment_records\(\) missing 2 required ",
                "positional arguments: 'values' and 'file'",
                )),
            self.database.set_segment_records,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "delete_segment_records\(\) missing 2 required ",
                "positional arguments: 'values' and 'file'",
                )),
            self.database.delete_segment_records,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "insert_segment_records\(\) missing 2 required ",
                "positional arguments: 'values' and 'file'",
                )),
            self.database.insert_segment_records,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_record_number\(\) takes from 2 to 4 ",
                "positional arguments but 5 were given",
                )),
            self.database.recordlist_record_number,
            *(None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_record_number_range\(\) takes from 2 to 5 ",
                "positional arguments but 6 were given",
                )),
            self.database.recordlist_record_number_range,
            *(None, None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_ebm\(\) takes from 2 to 3 ",
                "positional arguments but 4 were given",
                )),
            self.database.recordlist_ebm,
            *(None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_table_connection\(\) missing 1 required positional ",
                "argument: 'file'",
                )),
            self.database.get_table_connection,
            )

    def test_02_get_primary_record(self):
        self.assertEqual(self.database.get_primary_record('file1', None), None)

    def test_03_get_primary_record(self):
        self.assertEqual(self.database.get_primary_record('file1', 1), None)

    def test_04_get_primary_record(self):
        self.database.put('file1', None, 'new value')
        self.assertEqual(
            self.database.get_primary_record('file1', 1),
            (1, 'new value'))

    def test_05_remove_record_from_ebm(self):
        self.assertRaisesRegex(
            _sqlite.DatabaseError,
            "Existence bit map for segment does not exist",
            self.database.remove_record_from_ebm,
            *('file1', 2),
            )

    def test_06_remove_record_from_ebm(self):
        self.assertEqual(self.database.add_record_to_ebm('file1', 2), (0, 2))
        self.assertEqual(
            self.database.remove_record_from_ebm('file1', 2), (0, 2))

    def test_07_add_record_to_ebm(self):
        self.assertEqual(self.database.add_record_to_ebm('file1', 2), (0, 2))
        self.assertEqual(self.database.add_record_to_ebm('file1', 4), (0, 4))

    def test_08_get_high_record(self):
        self.assertEqual(self.database.get_high_record('file1'), None)

    def test_09_get_segment_records(self):
        self.database.insert_segment_records((12,), 'file1')
        self.assertEqual(self.database.get_segment_records(1, 'file1'), 12)

    def test_10_get_segment_records(self):
        self.database.insert_segment_records((12,), 'file1')
        self.assertRaisesRegex(
            _sqlite.DatabaseError,
            "Segment record 2 missing in 'file1'",
            self.database.get_segment_records,
            *(2, 'file1'),
            )

    def test_11_set_segment_records(self):
        self.database.insert_segment_records((12,), 'file1')
        self.database.set_segment_records((13, 1), 'file1')
        self.assertEqual(self.database.get_segment_records(1, 'file1'), 13)

    def test_12_delete_segment_records(self):
        self.database.delete_segment_records((12,), 'file1')

    def test_13_insert_segment_records(self):
        self.assertEqual(
            self.database.insert_segment_records((12,), 'file1'), 1)

    def test_14_recordset_record_number(self):
        self.assertIsInstance(
            self.database.recordlist_record_number('file1'),
            recordset.RecordList)

    def test_15_recordset_record_number(self):
        self.assertIsInstance(
            self.database.recordlist_record_number('file1', key=500),
            recordset.RecordList)

    def test_16_recordset_record_number(self):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1',
            '(',
            'file1', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        values = 1, 'Some value'
        cursor.execute(statement, values)
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        values = 1, b'\x740' + b'\x00' * (SegmentSize.db_segment_size_bytes - 1)
        cursor.execute(statement, values)
        rl = self.database.recordlist_record_number('file1', key=1)
        self.assertIsInstance(rl, recordset.RecordList)
        self.assertEqual(rl.count_records(), 1)

    def test_17_recordset_record_number_range(self):
        self.assertIsInstance(
            self.database.recordlist_record_number_range('file1'),
            recordset.RecordList)

    def test_18_recordset_record_number_range(self):
        self.create_ebm()
        rs = self.database.recordlist_record_number_range(
            'file1', keystart=0, keyend=2000)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(
            rs[0].tobytes(),
            b'\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

    def test_19_recordset_record_number_range(self):
        self.create_ebm()
        rs = self.database.recordlist_record_number_range(
            'file1', keystart=10)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(
            rs[0].tobytes(),
            b'\x00\x3f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

    def test_20_recordset_record_number_range(self):
        self.create_ebm()
        rs = self.database.recordlist_record_number_range(
            'file1', keyend=35)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(
            rs[0].tobytes(),
            b'\x7f\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_21_recordset_record_number_range(self):
        self.create_ebm()
        rs = self.database.recordlist_record_number_range(
            'file1', keystart=10, keyend=35)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(
            rs[0].tobytes(),
            b'\x00\x3f\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_22_recordset_record_number_range(self):
        self.create_ebm()
        self.create_ebm_extra(2)
        self.create_ebm_extra(3)
        self.create_ebm_extra(4)
        rs = self.database.recordlist_record_number_range(
            'file1', keystart=170, keyend=350)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(
            rs[1].tobytes(),
            b'\x00\x00\x00\x00\x00\x3f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        self.assertEqual(
            rs[2].tobytes(),
            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00')

    def test_23_recordset_record_number_range(self):
        self.create_ebm()
        self.create_ebm_extra(2)
        self.create_ebm_extra(3)
        self.create_ebm_extra(4)
        rs = self.database.recordlist_record_number_range(
            'file1', keystart=350, keyend=170)
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_24_recordset_ebm(self):
        self.assertIsInstance(
            self.database.recordlist_ebm('file1'),
            recordset.RecordList)

    def test_25_recordset_ebm(self):
        self.create_ebm()
        self.assertIsInstance(
            self.database.recordlist_ebm('file1'),
            recordset.RecordList)

    def test_26_get_table_connection(self):
        self.assertIsInstance(self.database.get_table_connection('file1'),
                              dbe_module.Connection)

    def create_ebm(self):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        values = 1, b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        cursor.execute(statement, values)

    def create_ebm_extra(self, segment):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        values = (segment,
                  b'\xff' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1))
        cursor.execute(statement, values)


class Database_find_values(_SQLiteOpen):

    def setUp(self):
        super().setUp()
        self.valuespec = ValuesClause()
        self.valuespec.field = 'field1'

    def test_01_find_values(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "find_values\(\) missing 2 required positional arguments: ",
                "'valuespec' and 'file'",
                )),
            self.database.find_values,
            )

    def test_02_find_values(self):
        self.valuespec.above_value = 'b'
        self.valuespec.below_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_03_find_values(self):
        self.valuespec.above_value = 'b'
        self.valuespec.to_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_04_find_values(self):
        self.valuespec.from_value = 'b'
        self.valuespec.to_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_05_find_values(self):
        self.valuespec.from_value = 'b'
        self.valuespec.below_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_06_find_values(self):
        self.valuespec.above_value = 'b'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_07_find_values(self):
        self.valuespec.from_value = 'b'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_08_find_values(self):
        self.valuespec.to_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_09_find_values(self):
        self.valuespec.below_value = 'd'
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_10_find_values(self):
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            [])

    def test_11_find_values(self):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1_field1',
            '(',
            'field1',
            ')',
            'values ( ? )',
            ))
        values = 'd',
        cursor.execute(statement, values)
        self.assertEqual(
            [i for i in self.database.find_values(self.valuespec, 'file1')],
            ['d'])


class Database_make_recordset(_SQLiteOpen):

    def setUp(self):
        super().setUp()
        segments = (
            b'\x7f\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00',
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00',
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff',
            b'\x00\x40\x00\x41',
            b'\x00\x42\x00\x43\x00\x44',
            )
        self.segments = {}
        keys = (
            'a_o',
            'aa_o',
            'ba_o',
            'bb_o',
            'c_o',
            'cep',
            'deq',
            )
        self.keyvalues = {}
        key_statement = " ".join((
            "insert into file1_field1 (",
            "field1", ",",
            "Segment", ",",
            "RecordCount", ",",
            "file1", ")",
            "values ( ? , ? , ? , ? )",
            ))
        cursor = self.database.dbenv.cursor()
        try:
            for s in segments:
                cursor.execute(
                    "insert into file1__segment ( RecordNumbers ) values ( ? )",
                    (s,))
                self.segments[
                    cursor.execute(
                        'select last_insert_rowid() from file1__segment'
                        ).fetchone()[0]] = s
            for e, k in enumerate(keys):
                self.keyvalues[k] = e + 1
                cursor.execute(
                    key_statement,
                    (k, 0, 32 if e else 31, self.keyvalues[k]))
            self.keyvalues['tww'] = 8
            cursor.execute(
                key_statement,
                ('tww', 0, 2, self.keyvalues['tww']))
            self.keyvalues['twy'] = 9
            cursor.execute(
                key_statement,
                ('twy', 0, 2, self.keyvalues['twy']))
            cursor.execute(
                key_statement,
                ('one', 0, 1, 50))
            cursor.execute(
                key_statement,
                ('nin', 0, 1, 100))
            cursor.execute(
                key_statement,
                ('www', 0, 2, self.keyvalues['twy']))
            cursor.execute(
                key_statement,
                ('www', 1, 2, self.keyvalues['twy']))
        finally:
            cursor.close()

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "add_record_to_field_value\(\) missing 5 required ",
                "positional arguments: 'file', 'field', 'key', 'segment', ",
                "and 'record_number'",
                )),
            self.database.add_record_to_field_value,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "remove_record_from_field_value\(\) missing 5 required ",
                "positional arguments: 'file', 'field', 'key', 'segment', ",
                "and 'record_number'",
                )),
            self.database.remove_record_from_field_value,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "populate_segment\(\) missing 2 required ",
                "positional arguments: 'segment_reference' and 'file'",
                )),
            self.database.populate_segment,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_key_like\(\) takes from 3 to 5 ",
                "positional arguments but 6 were given",
                )),
            self.database.recordlist_key_like,
            *(None, None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_key\(\) takes from 3 to 5 ",
                "positional arguments but 6 were given",
                )),
            self.database.recordlist_key,
            *(None, None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_key_startswith\(\) takes from 3 to 5 ",
                "positional arguments but 6 were given",
                )),
            self.database.recordlist_key_startswith,
            *(None, None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_key_range\(\) takes from 3 to 8 ",
                "positional arguments but 9 were given",
                )),
            self.database.recordlist_key_range,
            *(None, None, None, None, None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "recordlist_all\(\) takes from 3 to 4 ",
                "positional arguments but 5 were given",
                )),
            self.database.recordlist_all,
            *(None, None, None, None),
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "unfile_records_under\(\) missing 3 required ",
                "positional arguments: 'file', 'field', and 'key'",
                )),
            self.database.unfile_records_under,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "file_records_under\(\) missing 4 required positional ",
                "arguments: 'file', 'field', 'recordset', and 'key'",
                )),
            self.database.file_records_under,
            )

    def test_02_add_record_to_field_value(self):
        self.database.add_record_to_field_value(
            'file1', 'field1', 'indexvalue', 1, 0)

    def test_03_add_record_to_field_value(self):
        self.database.add_record_to_field_value(
            'file1', 'field1', 'nin', 0, 99)

    def test_04_add_record_to_field_value(self):
        self.database.add_record_to_field_value(
            'file1', 'field1', 'twy', 0, 99)

    def test_05_add_record_to_field_value(self):
        self.database.add_record_to_field_value(
            'file1', 'field1', 'aa_o', 0, 99)

    def test_06_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'indexvalue', 1, 0)

    def test_07_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'nin', 0, 99)

    def test_08_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'twy', 0, 68)

    def test_09_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'bb_o', 0, 68)

    def test_10_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'tww', 0, 65)

    def test_11_remove_record_from_field_value(self):
        self.database.remove_record_from_field_value(
            'file1', 'field1', 'one', 0, 50)

    def test_12_populate_segment(self):
        s = self.database.populate_segment(
            ('keyvalue' , 2, 1, 3),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentInt)

    def test_13_populate_segment(self):
        ss = ' '.join(('select field1 , Segment , RecordCount , file1 from',
                       'file1_field1 where field1 == "one" and Segment == 0',
                       ))
        s = self.database.populate_segment(
            self.database.dbenv.cursor().execute(ss).fetchone(),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentInt)

    def test_14_populate_segment(self):
        s = self.database.populate_segment(
            ('tww' , 0, 2, self.keyvalues['tww']),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentList)
        self.assertEqual(s.count_records(), 2)

    def test_15_populate_segment(self):
        ss = ' '.join(('select field1 , Segment , RecordCount , file1 from',
                       'file1_field1 where field1 == "tww" and Segment == 0',
                       ))
        s = self.database.populate_segment(
            self.database.dbenv.cursor().execute(ss).fetchone(),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentList)
        self.assertEqual(s.count_records(), 2)

    def test_16_populate_segment(self):
        s = self.database.populate_segment(
            ('c_o' , 0, 24, self.keyvalues['c_o']),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentBitarray)
        self.assertEqual(s.count_records(), 24)

    def test_17_populate_segment(self):
        ss = ' '.join(('select field1 , Segment , RecordCount , file1 from',
                       'file1_field1 where field1 == "c_o" and Segment == 0',
                       ))
        s = self.database.populate_segment(
            self.database.dbenv.cursor().execute(ss).fetchone(),
            'file1')
        self.assertIsInstance(s, recordset.RecordsetSegmentBitarray)
        self.assertEqual(s.count_records(), 24)

    def test_18_make_recordset_key_like(self):
        rs = self.database.recordlist_key_like('file1', 'field1')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_19_make_recordset_key_like(self):
        rs = self.database.recordlist_key_like(
            'file1', 'field1', keylike='z')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_20_make_recordset_key_like(self):
        rs = self.database.recordlist_key_like(
            'file1', 'field1', keylike='n')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 2)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_21_make_recordset_key_like(self):
        rs = self.database.recordlist_key_like(
            'file1', 'field1', keylike='w')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0].count_records(), 5)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_22_make_recordset_key_like(self):
        rs = self.database.recordlist_key_like(
            'file1', 'field1', keylike='e')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 41)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_23_make_recordset_key(self):
        rs = self.database.recordlist_key('file1', 'field1')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_24_make_recordset_key(self):
        rs = self.database.recordlist_key('file1', 'field1', key='one')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 1)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentInt)

    def test_25_make_recordset_key(self):
        rs = self.database.recordlist_key('file1', 'field1', key='tww')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 2)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentList)

    def test_26_make_recordset_key(self):
        rs = self.database.recordlist_key('file1', 'field1', key='a_o')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 31)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_27_make_recordset_key_startswith(self):
        rs = self.database.recordlist_key_startswith('file1', 'field1')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_28_make_recordset_key_startswith(self):
        rs = self.database.recordlist_key_startswith(
            'file1', 'field1', keystart='ppp')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_29_make_recordset_key_startswith(self):
        rs = self.database.recordlist_key_startswith(
            'file1', 'field1', keystart='o')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(rs[0].count_records(), 1)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentInt)

    def test_30_make_recordset_key_startswith(self):
        rs = self.database.recordlist_key_startswith(
            'file1', 'field1', keystart='tw')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(rs[0].count_records(), 5)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_31_make_recordset_key_startswith(self):
        rs = self.database.recordlist_key_startswith(
            'file1', 'field1', keystart='d')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(rs[0].count_records(), 24)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_32_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range('file1', 'field1')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0].count_records(), 127)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_33_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='ppp', le='qqq')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_34_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='n', le='q')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 2)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_35_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='t', le='tz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 5)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_36_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='c', le='cz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 40)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_37_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='c')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0].count_records(), 62)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_38_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', le='cz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 111)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_39_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', ge='ppp', lt='qqq')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_40_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', gt='ppp', lt='qqq')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 0)

    def test_41_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', gt='n', le='q')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 2)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_42_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', gt='t', le='tz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 5)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_43_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', gt='c', lt='cz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 40)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_44_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', gt='c')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0].count_records(), 62)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_45_make_recordset_key_range(self):
        rs = self.database.recordlist_key_range(
            'file1', 'field1', lt='cz')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].count_records(), 111)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_46_make_recordset_all(self):
        rs = self.database.recordlist_all('file1', 'field1')
        self.assertIsInstance(rs, recordset.RecordList)
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0].count_records(), 127)
        self.assertIsInstance(rs[0], recordset.RecordsetSegmentBitarray)

    def test_47_unfile_records_under(self):
        self.database.unfile_records_under('file1', 'field1', 'aa_o')

    def test_48_unfile_records_under(self):
        self.database.unfile_records_under('file1', 'field1', 'kkkk')

    def test_49_file_records_under(self):
        rs = self.database.recordlist_all('file1', 'field1')
        self.database.file_records_under('file1', 'field1', rs, 'aa_o')

    def test_50_file_records_under(self):
        rs = self.database.recordlist_all('file1', 'field1')
        self.database.file_records_under('file1', 'field1', rs, 'rrr')

    def test_51_file_records_under(self):
        rs = self.database.recordlist_key('file1', 'field1', key='twy')
        self.database.file_records_under('file1', 'field1', rs, 'aa_o')

    def test_52_file_records_under(self):
        rs = self.database.recordlist_key('file1', 'field1', key='twy')
        self.database.file_records_under('file1', 'field1', rs, 'rrr')

    def test_53_file_records_under(self):
        rs = self.database.recordlist_key('file1', 'field1', key='one')
        self.database.file_records_under('file1', 'field1', rs, 'aa_o')

    def test_54_file_records_under(self):
        rs = self.database.recordlist_key('file1', 'field1', key='one')
        self.database.file_records_under('file1', 'field1', rs, 'rrr')

    def test_55_file_records_under(self):
        rs = self.database.recordlist_key('file1', 'field1', key='ba_o')
        self.database.file_records_under('file1', 'field1', rs, 'www')

    def test_56_database_cursor(self):
        d = self.database
        self.assertIsInstance(d.database_cursor('file1', 'file1'),
                              _sqlite.CursorPrimary)
        self.assertIsInstance(d.database_cursor('file1', 'field1'),
                              _sqlite.CursorSecondary)

    def test_57_create_recordset_cursor(self):
        d = self.database
        rs = self.database.recordlist_key('file1', 'field1', key=b'ba_o')
        self.assertIsInstance(d.create_recordset_cursor(rs),
                              recordset.RecordsetCursor)


class Database_freed_record_number(_SQLiteOpen):

    def setUp(self):
        super().setUp()
        self.database.ebm_control['file1'] = _sqlite.ExistenceBitmapControl(
            'file1', self.database)
        self.statement = ' '.join((
            'insert into',
            'file1',
            '(',
            'file1', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        cursor = self.database.dbenv.cursor()
        for i in range(SegmentSize.db_segment_size * 3 - 1):
            cursor.execute(self.statement,
                           (None, '_'.join((str(i + 1), 'value'))))
            self.database.add_record_to_ebm('file1', i + 1)
        cursor.close()
        self.high_record = self.database.get_high_record('file1')
        self.database.ebm_control['file1'].segment_count = divmod(
            self.high_record[0], SegmentSize.db_segment_size)[0]

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_lowest_freed_record_number\(\) missing 1 required ",
                "positional argument: 'dbset'",
                )),
            self.database.get_lowest_freed_record_number,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "note_freed_record_number_segment\(\) missing 4 required ",
                "positional arguments: 'dbset', 'segment', ",
                "'record_number_in_segment', and 'high_record'",
                )),
            self.database.note_freed_record_number_segment,
            )

    def test_02_note_freed_record_number_segment(self):
        self.assertEqual(
            self.database.ebm_control['file1'].freed_record_number_pages,
            None)
        for i in 100, 101, 200, 300,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        self.assertEqual(
            self.database.ebm_control['file1'].freed_record_number_pages,
            [0, 1, 2])
        self.database.ebm_control['file1'].freed_record_number_pages = None
        self.assertEqual(
            self.database.ebm_control['file1'].freed_record_number_pages,
            None)
        for i in 201,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        self.assertEqual(
            self.database.ebm_control['file1'].freed_record_number_pages,
            [0, 1, 2])

    def test_03_get_lowest_freed_record_number(self):
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, None)

    def test_04_get_lowest_freed_record_number(self):
        for i in 100, 101, 200, 300,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, 100)

    def test_05_get_lowest_freed_record_number(self):
        for i in 380,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, None)

    def test_06_get_lowest_freed_record_number(self):
        for i in 110,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, 110)

    # The freed record number in segment number 2, 'divmod(380, 128)', is not
    # seen until segment number 4 has records.
    # Segment 2 is not deleted from the 'freed record number' list until the
    # first search of the segment after all freed record numbers have been
    # re-used.
    def test_07_get_lowest_freed_record_number(self):
        self.assertEqual(self.database.ebm_control[
            'file1'].freed_record_number_pages, None)
        for i in 380,:
            self.database.delete('file1', i, '_'.join((str(i), 'value')))
            sn, rn = self.database.remove_record_from_ebm('file1', i)
            self.database.note_freed_record_number_segment(
                'file1', sn, rn, self.high_record)
        self.assertEqual(len(self.database.ebm_control[
            'file1'].freed_record_number_pages), 1)
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, None)
        i = self.high_record[0]
        cursor = self.database.dbenv.cursor()
        for i in range(i, i + 129):
            cursor.execute(self.statement,
                           (None, '_'.join((str(i + 1), 'value'))))
            self.database.add_record_to_ebm('file1', i + 1)
        cursor.close()
        self.assertEqual(len(self.database.ebm_control[
            'file1'].freed_record_number_pages), 1)
        self.high_record = self.database.get_high_record('file1')
        self.database.ebm_control['file1'].segment_count = divmod(
            self.high_record[0], SegmentSize.db_segment_size)[0]
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, 380)
        self.assertEqual(len(self.database.ebm_control[
            'file1'].freed_record_number_pages), 1)
        self.database.add_record_to_ebm('file1', 380)
        rn = self.database.get_lowest_freed_record_number('file1')
        self.assertEqual(rn, None)
        self.assertEqual(len(self.database.ebm_control[
            'file1'].freed_record_number_pages), 0)


# Does this test add anything beyond Database_freed_record_number?
class Database_empty_freed_record_number(_SQLiteOpen):

    def setUp(self):
        super().setUp()
        self.high_record = self.database.get_high_record('file1')

    def test_01(self):
        self.assertEqual(self.database.ebm_control[
            'file1'].freed_record_number_pages, None)
        self.database.note_freed_record_number_segment(
            'file1', 0, 100, self.high_record)
        self.assertEqual(self.database.ebm_control[
            'file1'].freed_record_number_pages, None)
        self.assertEqual(self.database.get_high_record('file1'),
                         self.high_record)


class RecordsetCursor(_SQLiteOpen):

    def setUp(self):
        super().setUp()
        segments = (
            b'\x7f\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00',
            )
        keys = (
            'a_o',
            )
        key_statement = " ".join((
            "insert into file1_field1 (",
            "field1", ",",
            "Segment", ",",
            "RecordCount", ",",
            "file1", ")",
            "values ( ? , ? , ? , ? )",
            ))
        cursor = self.database.dbenv.cursor()
        try:
            for i in range(380):
                cursor.execute(
                    "insert into file1 ( Value ) values ( ? )",
                    (str(i +1) + "Any value",))
            statement = ' '.join((
                'insert into',
                'file1__ebm',
                '(',
                'file1__ebm', ',', 'Value',
                ')',
                'values ( ? , ? )',
                ))
            bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
            cursor.execute(statement, (1, bits))
            bits = b'\xff' * SegmentSize.db_segment_size_bytes
            cursor.execute(statement, (2, bits))
            cursor.execute(statement, (3, bits))
            for s in segments:
                cursor.execute(
                    "insert into file1__segment ( RecordNumbers ) values ( ? )",
                    (s,))
            for e in range(len(segments)):
                cursor.execute(
                    key_statement,
                    ('a_o', e, 32 if e else 31, e + 1))
        finally:
            cursor.close()

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "__init__\(\) missing 2 required ",
                "positional arguments: 'recordset' and 'engine'",
                )),
            _sqlite.RecordsetCursor,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "_get_record\(\) missing 1 required ",
                "positional argument: 'record_number'",
                )),
            _sqlite.RecordsetCursor(None, None)._get_record,
            )

    def test_02___init__01(self):
        rc = _sqlite.RecordsetCursor(None, True)
        self.assertEqual(rc.engine, True)

    def test_03___init__02(self):
        rs = self.database.recordlist_key('file1', 'field1', key='a_o')
        rc = _sqlite.RecordsetCursor(rs, self.database.dbenv)
        self.assertIs(rc.engine, self.database.dbenv)
        self.assertIs(rc._dbset, rs)

    def test_04__get_record(self):
        rc = _sqlite.RecordsetCursor(
            self.database.recordlist_key('file1', 'field1', key='a_o'),
            self.database.dbenv)
        self.assertEqual(rc._get_record(4000), None)
        self.assertEqual(rc._get_record(120), None)
        self.assertEqual(rc._get_record(10), (10, '10Any value'))
        self.assertEqual(rc._get_record(155), (155, '155Any value'))


class ExistenceBitmapControl(_SQLiteOpen):

    def setUp(self):
        super().setUp()

    def test_01(self):
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "read_exists_segment\(\) missing 2 required ",
                "positional arguments: 'segment_number' and 'dbenv'",
                )),
            self.database.ebm_control['file1'].read_exists_segment,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "get_ebm_segment\(\) missing 2 required ",
                "positional arguments: 'key' and 'dbenv'",
                )),
            self.database.ebm_control['file1'].get_ebm_segment,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "delete_ebm_segment\(\) missing 2 required ",
                "positional arguments: 'key' and 'dbenv'",
                )),
            self.database.ebm_control['file1'].delete_ebm_segment,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "put_ebm_segment\(\) missing 3 required ",
                "positional arguments: 'key', 'value', and 'dbenv'",
                )),
            self.database.ebm_control['file1'].put_ebm_segment,
            )
        self.assertRaisesRegex(
            TypeError,
            "".join((
                "append_ebm_segment\(\) missing 2 required ",
                "positional arguments: 'value' and 'dbenv'",
                )),
            self.database.ebm_control['file1'].append_ebm_segment,
            )

    def test_02_read_exists_segment_01(self):
        self.assertEqual(self.database.ebm_control['file1']._segment_count, 0)
        self.assertEqual(
            self.database.ebm_control['file1'].read_exists_segment(
                0, self.database.dbenv),
            None)

    def test_03_read_exists_segment_02(self):
        self.assertEqual(self.database.ebm_control['file1']._segment_count, 0)
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        cursor.execute(statement, (1, bits))
        bits = b'\xff' * SegmentSize.db_segment_size_bytes
        cursor.execute(statement, (2, bits))
        cursor.execute(statement, (3, bits))
        self.database.ebm_control['file1']._segment_count = 3
        seg = self.database.ebm_control['file1'].read_exists_segment(
            0, self.database.dbenv)
        self.assertEqual(seg.count(), 127)
        seg = self.database.ebm_control['file1'].read_exists_segment(
            1, self.database.dbenv)
        self.assertEqual(seg.count(), 128)

    def test_04_get_ebm_segment_01(self):
        sr = self.database.ebm_control['file1'].get_ebm_segment(
            0, self.database.dbenv)
        self.assertEqual(sr, None)

    def test_05_get_ebm_segment_02(self):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        cursor.execute(statement, (1, bits))
        sr = self.database.ebm_control['file1'].get_ebm_segment(
            1, self.database.dbenv)
        self.assertEqual(sr, bits)

    def test_06_delete_ebm_segment_01(self):
        self.database.ebm_control['file1'].delete_ebm_segment(
            0, self.database.dbenv)

    def test_07_delete_ebm_segment_02(self):
        cursor = self.database.dbenv.cursor()
        statement = ' '.join((
            'insert into',
            'file1__ebm',
            '(',
            'file1__ebm', ',', 'Value',
            ')',
            'values ( ? , ? )',
            ))
        bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        cursor.execute(statement, (1, bits))
        self.database.ebm_control['file1'].delete_ebm_segment(
            1, self.database.dbenv)

    def test_08_put_ebm_segment(self):
        bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        self.database.ebm_control['file1'].put_ebm_segment(
            0, bits, self.database.dbenv)

    def test_09_append_ebm_segment(self):
        bits = b'\x7f' + b'\xff' * (SegmentSize.db_segment_size_bytes - 1)
        self.database.ebm_control['file1'].append_ebm_segment(
            bits, self.database.dbenv)


if __name__ == '__main__':
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    for dbe_module in sqlite3, apsw:
        if dbe_module is None:
            continue
        runner().run(loader(Database___init__))
        runner().run(loader(Database_transaction_methods))
        runner().run(loader(DatabaseInstance))
        runner().run(loader(Database_open_database))
        runner().run(loader(Database_do_database_task))
        runner().run(loader(DatabaseTransactions))
        runner().run(loader(Database_put_replace_delete))
        runner().run(loader(Database_methods))
        runner().run(loader(Database_find_values))
        runner().run(loader(Database_make_recordset))
        runner().run(loader(Database_freed_record_number))
        runner().run(loader(Database_empty_freed_record_number))
        runner().run(loader(RecordsetCursor))
        runner().run(loader(ExistenceBitmapControl))
