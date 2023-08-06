import unittest
from FixedWidthTextParser.Seismic.VibratorParser import ApsParser, CogParser, VapsParser


class ApsParserTest(unittest.TestCase):
    def test_parse_point(self):
        parser = ApsParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        data = parser.parse_point(record)

        self.assertIsNone(data)

        record = 'A         19064.0 25360.01222 70   1   2101863 71 56 72 725883.0 2531118.2 121.6'
        data = parser.parse_point(record)

        self.assertEqual('A', data[0])
        self.assertEqual(19064.0, data[1])
        self.assertEqual(25360.0, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual(2, data[4])
        self.assertEqual(22, data[5])
        self.assertEqual(70, data[6])
        self.assertEqual(1, data[7])
        self.assertEqual(2, data[8])
        self.assertEqual(10, data[9])
        self.assertEqual(18, data[10])
        self.assertEqual(63, data[11])
        self.assertEqual(71, data[12])
        self.assertEqual(56, data[13])
        self.assertEqual(72, data[14])
        self.assertEqual(725883.0, data[15])
        self.assertEqual(2531118.2, data[16])
        self.assertEqual(121.6, data[17])

    def test_parse_point2obj(self):
        parser = ApsParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        obj = parser.parse_point2obj(record)

        self.assertIsNone(obj)

        record = 'A         19064.0 25360.01222 70   1   2101863 71 56 72 725883.0 2531118.2 121.6'
        obj = parser.parse_point2obj(record)

        self.assertEqual('A', obj.type)
        self.assertEqual(19064.0, obj.line)
        self.assertEqual(25360.0, obj.point)
        self.assertEqual(1, obj.point_idx)
        self.assertEqual(2, obj.vib_fleet_no)
        self.assertEqual(22, obj.vib_no)
        self.assertEqual(70, obj.vib_drive_level)
        self.assertEqual(1, obj.phase_avg)
        self.assertEqual(2, obj.phase_peak)
        self.assertEqual(10, obj.dist_avg)
        self.assertEqual(18, obj.dist_peak)
        self.assertEqual(63, obj.force_avg)
        self.assertEqual(71, obj.force_peak)
        self.assertEqual(56, obj.stiff)
        self.assertEqual(72, obj.visc)
        self.assertEqual(725883.0, obj.easting)
        self.assertEqual(2531118.2, obj.northing)
        self.assertEqual(121.6, obj.elevation)


class CogParserTest(unittest.TestCase):
    def test_parse_point(self):
        parser = CogParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        data = parser.parse_point(record)

        self.assertIsNone(data)

        record = 'C         19064.0 25360.01 3  725883.0  2531118.2  121.6          2.5'
        data = parser.parse_point(record)

        self.assertEqual('C', data[0])
        self.assertEqual(19064.0, data[1])
        self.assertEqual(25360.0, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual(3, data[4])
        self.assertEqual(725883.0, data[5])
        self.assertEqual(2531118.2, data[6])
        self.assertEqual(121.6, data[7])
        self.assertEqual(2.5, data[8])

    def test_parse_point2obj(self):
        parser = CogParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        obj = parser.parse_point2obj(record)

        self.assertIsNone(obj)

        record = 'C         19064.0 25360.01 3  725883.0  2531118.2  121.6          2.5'
        obj = parser.parse_point2obj(record)

        self.assertEqual('C', obj.type)
        self.assertEqual(19064.0, obj.line)
        self.assertEqual(25360.0, obj.point)
        self.assertEqual(1, obj.point_idx)
        self.assertEqual(3, obj.cog_state)
        self.assertEqual(725883.0, obj.easting)
        self.assertEqual(2531118.2, obj.northing)
        self.assertEqual(121.6, obj.elevation)
        self.assertEqual(2.5, obj.deviation)


class VapsParserTest(unittest.TestCase):
    def test_parse_point(self):
        parser = VapsParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        data = parser.parse_point(record)

        self.assertIsNone(data)

        record = 'A         19080.0 25206.01222 70   1  -3111864 73 55 73 723954.7 2531266.3 124.4     1 122 1                   1T 4.1294035708 1.1    1287187046624000GPGGA,235726.00,2252.45969167,N,05310.97627209,E,4,10,1.1,127.602,M,-33.537,M,9.0,0002*67'
        data = parser.parse_point(record)

        self.assertEqual('A', data[0])
        self.assertEqual(19080.0, data[1])
        self.assertEqual(25206.0, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual(2, data[4])
        self.assertEqual(22, data[5])
        self.assertEqual(70, data[6])
        self.assertEqual(1, data[7])
        self.assertEqual(-3, data[8])
        self.assertEqual(11, data[9])
        self.assertEqual(18, data[10])
        self.assertEqual(64, data[11])
        self.assertEqual(73, data[12])
        self.assertEqual(55, data[13])
        self.assertEqual(73, data[14])
        self.assertEqual(723954.7, data[15])
        self.assertEqual(2531266.3, data[16])
        self.assertEqual(124.4, data[17])
        self.assertEqual(1, data[18])
        self.assertEqual(1, data[19])
        self.assertEqual(22, data[20])
        self.assertEqual(1, data[21])
        self.assertEqual(None, data[22])
        self.assertEqual(None, data[23])
        self.assertEqual(None, data[24])
        self.assertEqual(None, data[25])
        self.assertEqual(None, data[26])
        self.assertEqual(None, data[27])
        self.assertEqual(None, data[28])
        self.assertEqual(None, data[29])
        self.assertEqual(None, data[30])
        self.assertEqual(None, data[31])
        self.assertEqual(None, data[32])
        self.assertEqual(None, data[33])
        self.assertEqual(None, data[34])
        self.assertEqual(None, data[35])
        self.assertEqual(1, data[36])
        self.assertEqual('T', data[37])
        self.assertEqual('4.1', data[38])
        self.assertEqual(294, data[39])
        self.assertEqual('035708', data[40])
        self.assertEqual(1.1, data[41])
        self.assertEqual(1287187046624000, data[42])
        self.assertEqual('GPGGA,235726.00,2252.45969167,N,05310.97627209,E,4,10,1.1,127.602,M,-33.537,M,9.0,0002*67',
                         data[43])

    def test_parse_point2obj(self):
        parser = VapsParser()

        record = 'H26 5678901234567890123456789012345678901234567890123456789012345678901234567890'
        obj = parser.parse_point2obj(record)

        self.assertIsNone(obj)

        record = 'A         19080.0 25206.01222 70   1  -3111864 73 55 73 723954.7 2531266.3 124.4     1 122 1                   1T 4.1294035708 1.1    1287187046624000GPGGA,235726.00,2252.45969167,N,05310.97627209,E,4,10,1.1,127.602,M,-33.537,M,9.0,0002*67'
        obj = parser.parse_point2obj(record)

        self.assertEqual('A', obj.type)
        self.assertEqual(19080.0, obj.line)
        self.assertEqual(25206.0, obj.point)
        self.assertEqual(1, obj.point_idx)
        self.assertEqual(2, obj.vib_fleet_no)
        self.assertEqual(22, obj.vib_no)
        self.assertEqual(70, obj.vib_drive_level)
        self.assertEqual(1, obj.phase_avg)
        self.assertEqual(-3, obj.phase_peak)
        self.assertEqual(11, obj.dist_avg)
        self.assertEqual(18, obj.dist_peak)
        self.assertEqual(64, obj.force_avg)
        self.assertEqual(73, obj.force_peak)
        self.assertEqual(55, obj.stiff)
        self.assertEqual(73, obj.visc)
        self.assertEqual(723954.7, obj.easting)
        self.assertEqual(2531266.3, obj.northing)
        self.assertEqual(124.4, obj.elevation)
        self.assertEqual(1, obj.shot_no)
        self.assertEqual(1, obj.acquisition_no)
        self.assertEqual(22, obj.vib_fleet_no2)
        self.assertEqual(1, obj.vib_status_code)
        self.assertEqual(None, obj.mass_1_w)
        self.assertEqual(None, obj.mass_2_w)
        self.assertEqual(None, obj.mass_3_w)
        self.assertEqual(None, obj.plate_1_w)
        self.assertEqual(None, obj.plate_2_w)
        self.assertEqual(None, obj.plate_3_w)
        self.assertEqual(None, obj.plate_4_w)
        self.assertEqual(None, obj.plate_5_w)
        self.assertEqual(None, obj.plate_6_w)
        self.assertEqual(None, obj.force_overload)
        self.assertEqual(None, obj.pressure_overload)
        self.assertEqual(None, obj.mass_overload)
        self.assertEqual(None, obj.valve_overload)
        self.assertEqual(None, obj.excitation_overload)
        self.assertEqual(1, obj.stacking_folder)
        self.assertEqual('T', obj.computation_domain)
        self.assertEqual('4.1', obj.ve_version)
        self.assertEqual(294, obj.day_of_year)
        self.assertEqual('035708', obj.time)
        self.assertEqual(1.1, obj.hdop)
        self.assertEqual(1287187046624000, obj.tb_date)
        self.assertEqual('GPGGA,235726.00,2252.45969167,N,05310.97627209,E,4,10,1.1,127.602,M,-33.537,M,9.0,0002*67',
                         obj.gpgga_message)
