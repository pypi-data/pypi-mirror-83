import unittest
from FixedWidthTextParser.Parser import Parser

definition = {
    'FIELD_1': [0, 1, 'string'],
    'FIELD_2': [1, 10, 'float'],
    'FIELD_3': [11, 10, 'float'],
    'FIELD_4': [23, 1, 'integer'],
    'FIELD_5': [24, 2, 'string'],
    'FIELD_6': [26, 4, 'integer', 0],
    'FIELD_7': [30, 4, 'integer', None],
    'FIELD_8': [34, 4, 'float', None],
    'FIELD_9': [38, 4, 'float', 0.0],
    'FIELD_10': [42, 2, 'string', None],
    'FIELD_11': [44, 2, 'string', ''],
}


class ParserTest(unittest.TestCase):
    def test_parse_empty_format(self):
        parser = Parser()
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        with self.assertRaises(Exception):
            parser.parse(record)

    def test_parse(self):
        parser = Parser(definition)
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        data = parser.parse(record)

        self.assertEqual('S', data[0])
        self.assertEqual(21528.00, data[1])
        self.assertEqual(27830.00, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual('P1', data[4])
        self.assertEqual(0, data[5])
        self.assertEqual(None, data[6])
        self.assertEqual(None, data[7])
        self.assertEqual(0.0, data[8])
        self.assertEqual(None, data[9])
        self.assertEqual('', data[10])

    def test_csv_from_array(self):
        parser = Parser(definition)

        data = parser.get_fields()
        csv = parser.csv_from_array(data)
        self.assertEqual('FIELD_1,FIELD_2,FIELD_3,FIELD_4,FIELD_5,FIELD_6,FIELD_7,FIELD_8,FIELD_9,FIELD_10,FIELD_11',
                         csv)

    def test_array_from_csv(self):
        parser = Parser(definition)

        csv = 'FIELD_1,FIELD_2,FIELD_3,FIELD_4,FIELD_5,FIELD_6,FIELD_7,FIELD_8'
        data = parser.array_from_csv(csv, ',')

        self.assertEqual('FIELD_1', data[0])
        self.assertEqual('FIELD_8', data[7])

    def test_parse2object(self):
        parser = Parser(definition)
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        obj = parser.parse2object(record)

        self.assertEqual('S', obj.FIELD_1)
        self.assertEqual(21528.0, obj.FIELD_2)
        self.assertEqual(27830.0, obj.FIELD_3)
        self.assertEqual(1, obj.FIELD_4)
        self.assertEqual('P1', obj.FIELD_5)
        self.assertEqual(0, obj.FIELD_6)
        self.assertEqual(None, obj.FIELD_7)
        self.assertEqual(None, obj.FIELD_8)
        self.assertEqual(0.0, obj.FIELD_9)
        self.assertEqual(None, obj.FIELD_10)
        self.assertEqual('', obj.FIELD_11)


if __name__ == '__main__':
    unittest.main()
