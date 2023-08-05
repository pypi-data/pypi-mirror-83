import os
from pathlib import Path
from unittest import TestCase
from pydbml import PyDBML
from pydbml.exceptions import TableNotFoundError, ColumnNotFoundError


TEST_DATA_PATH = Path(os.path.abspath(__file__)).parent / 'test_data'


class TestRefs(TestCase):
    def setUp(self):
        self.results = PyDBML.parse_file(TEST_DATA_PATH / 'general.dbml')

    def test_table_refs(self):
        p = PyDBML.parse_file(TEST_DATA_PATH / 'general.dbml')
        r = p['order_items'].refs
        self.assertEqual(r[0].col.name, 'order_id')
        self.assertEqual(r[0].ref_table.name, 'orders')
        self.assertEqual(r[0].ref_col.name, 'id')
        r = p['products'].refs
        self.assertEqual(r[0].col.name, 'merchant_id')
        self.assertEqual(r[0].ref_table.name, 'merchants')
        self.assertEqual(r[0].ref_col.name, 'id')
        r = p['users'].refs
        self.assertEqual(r[0].col.name, 'country_code')
        self.assertEqual(r[0].ref_table.name, 'countries')
        self.assertEqual(r[0].ref_col.name, 'code')

    def test_refs(self):
        p = PyDBML.parse_file(TEST_DATA_PATH / 'general.dbml')
        r = p.refs
        self.assertEqual(r[0].table1.name, 'orders')
        self.assertEqual(r[0].col1.name, 'id')
        self.assertEqual(r[0].table2.name, 'order_items')
        self.assertEqual(r[0].col2.name, 'order_id')
        self.assertEqual(r[2].table1.name, 'users')
        self.assertEqual(r[2].col1.name, 'country_code')
        self.assertEqual(r[2].table2.name, 'countries')
        self.assertEqual(r[2].col2.name, 'code')
        self.assertEqual(r[4].table1.name, 'products')
        self.assertEqual(r[4].col1.name, 'merchant_id')
        self.assertEqual(r[4].table2.name, 'merchants')
        self.assertEqual(r[4].col2.name, 'id')


class TestFaulty(TestCase):
    def test_bad_reference(self):
        with self.assertRaises(TableNotFoundError):
            PyDBML(TEST_DATA_PATH / 'wrong_inline_ref_table.dbml')
        with self.assertRaises(ColumnNotFoundError):
            PyDBML(TEST_DATA_PATH / 'wrong_inline_ref_column.dbml')

    def test_bad_index(self):
        with self.assertRaises(ColumnNotFoundError):
            PyDBML(TEST_DATA_PATH / 'wrong_index.dbml')
