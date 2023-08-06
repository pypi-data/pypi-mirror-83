# Copyright (c) 2018, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import unittest
import logging
from datetime import datetime, time, date

from geopathfinder.naming_conventions.yeoda_naming import YeodaFilename
from geopathfinder.naming_conventions.yeoda_naming import yeoda_path
from geopathfinder.naming_conventions.yeoda_naming import yeoda_tree

logging.basicConfig(level=logging.INFO)


class TestYeodaFilename(unittest.TestCase):

    def setUp(self):
        self.dtime_1 = datetime(2008, 1, 1, 12, 23, 33)
        self.dtime_2 = datetime(2009, 2, 2, 22, 1, 1)

        fields = {'datetime_1': self.dtime_1, 'datetime_2': self.dtime_2, 'var_name': 'SSM'}

        self.yeoda_fn = YeodaFilename(fields, convert=True)

        fields = {'datetime_1': self.dtime_1, 'var_name': 'SSM', 'band': 'VV'}

        self.yeoda_fn2 = YeodaFilename(fields, convert=True)

        self.yeoda_fn3 = YeodaFilename(fields)

        fn = 'SIG0_20170725T165004__VV_A146_E048N012T6_EU500M_V04R01_S1BIWG1.tif'
        self.yeoda_fn4 = YeodaFilename.from_filename(fn, convert=True)

        fn = 'TMENSIG40_20170725_20181225__A146_E048N012T6_EU500M__ASAWS.tif'
        self.yeoda_fn5 = YeodaFilename.from_filename(fn)

        fn = 'TMENSIG40_20170725_20181225_M1__E048N012T6_EU500M_V04R01_ASAWS.tif'
        self.yeoda_fn6 = YeodaFilename.from_filename(fn, convert=True)


    def test1_build_yeoda_filename(self):
        """
        Test building Yeoda file name.

        """
        fn = ('SSM_20080101T122333_20090202T220101______.tif')

        self.assertEqual(str(self.yeoda_fn), fn)


    def test2_get_n_set_date(self):
        """
        Test set and get start and end date.

        """
        self.assertEqual(self.yeoda_fn['datetime_1'], self.dtime_1)
        self.assertEqual(self.yeoda_fn['datetime_2'], self.dtime_2)

        new_start_time = datetime(2009, 1, 1, 12, 23, 33)
        self.yeoda_fn['datetime_1'] = new_start_time

        self.assertEqual(self.yeoda_fn['datetime_1'], new_start_time)
        self.assertEqual(self.yeoda_fn['datetime_2'], self.dtime_2)

    def test30_get_n_set_date_n_time(self):
        """
        Test set and get date and time for a single datetime.

        """
        self.assertEqual(self.yeoda_fn2['datetime_1'].date(), self.dtime_1.date())
        self.assertEqual(self.yeoda_fn2['datetime_1'].time(), self.dtime_1.time())

        new_start_time = datetime(2009, 1, 1, 12, 23, 33)
        self.yeoda_fn2['datetime_1'] = new_start_time

        self.assertEqual(self.yeoda_fn2['datetime_1'].date(), new_start_time.date())
        self.assertEqual(self.yeoda_fn2['datetime_1'].time(), new_start_time.time())

    def test31_get_n_set_date_n_time_dts(self):
        """
        Test get and set date and time for a single datetime,
        returning strings.

        """
        self.assertEqual(self.yeoda_fn2.obj.datetime_1.date(), datetime(2008, 1, 1).date())
        self.assertEqual(self.yeoda_fn2.obj.datetime_1.time(), time(12, 23, 33))

        new_start_time = date(2345, 1, 2)
        self.yeoda_fn2['datetime_1'] = new_start_time

        self.assertEqual(self.yeoda_fn2.obj.datetime_1.time(), time())

    def test32_get_n_set_date_n_time_strings(self):
        """
        Test get and set date and time for a single datetime,
        returning strings.

        """

        self.assertEqual(self.yeoda_fn3.obj.datetime_1, '20080101T122333')

        new_start_time = datetime(2345, 1, 2, 7, 8, 9)
        self.yeoda_fn3['datetime_2'] = new_start_time

        self.assertEqual(self.yeoda_fn3.obj.datetime_1, '20080101T122333')
        self.assertEqual(self.yeoda_fn3.obj.datetime_2, '23450102T070809')

    def test4_create_yeoda_filename(self):
        """
        Tests the creation of a SmartFilename from a given string filename.

        """

        # testing for single datetime
        self.assertEqual(self.yeoda_fn4['datetime_1'].date(), datetime(2017, 7, 25).date())
        self.assertEqual(self.yeoda_fn4['datetime_1'].time(), time(16, 50, 4))
        self.assertEqual(self.yeoda_fn4['var_name'], 'SIG0')
        self.assertEqual(self.yeoda_fn4['sensor_field'], 'S1BIWG1')
        self.assertEqual(self.yeoda_fn4['band'], 'VV')
        self.assertEqual(self.yeoda_fn4['extra_field'], 'A146')
        self.assertEqual(self.yeoda_fn4['version_run_id'], 'V04R01')
        self.assertEqual(self.yeoda_fn4['grid_name'], 'EU500M')
        self.assertEqual(self.yeoda_fn4['tile_name'], 'E048N012T6')
        self.assertEqual(self.yeoda_fn4.ext, '.tif')

        # testing for empty fields and two dates
        self.assertEqual(self.yeoda_fn5['datetime_1'], '20170725')
        self.assertEqual(self.yeoda_fn5['datetime_2'], '20181225')
        self.assertEqual(self.yeoda_fn5['var_name'], 'TMENSIG40')
        self.assertEqual(self.yeoda_fn5['sensor_field'], 'ASAWS')
        self.assertEqual(self.yeoda_fn5['band'], '')
        self.assertEqual(self.yeoda_fn5['version_run_id'], '')

        # testing for empty relative orbit field
        self.assertEqual(self.yeoda_fn6['extra_field'], None)

    def test5_build_ascat_ssm_fname(self):
        """
        Tests the creation of a resampled ASCAT SSM filename.

        """
        date_time = '20331122_112233'
        tilename = 'EU500M_E012N024T6'

        xfields = {'datetime_1': datetime.strptime(date_time, "%Y%m%d_%H%M%S"),
                   'var_name': 'SSM',
                   'sensor_field': 'ASCSMO12NA',
                   'band': 'XX',
                   'extra_field': 'D',
                   'version_run_id': 'V02R01',
                   'grid_name': tilename[:6],
                   'tile_name': tilename[7:]}

        should = 'SSM_20331122T112233__XX_D_E012N024T6_EU500M_V02R01_ASCSMO12NA.tif'
        fn = YeodaFilename(xfields)
        self.assertEqual(str(fn), should)

    def test6_compact_fname(self):
        """
        Tests if the compact representation of the filename works as expected.

        """
        self.yeoda_fn4['version_run_id'] = 'R01'
        fn_str = str(self.yeoda_fn4)
        self.assertEqual(fn_str, 'SIG0_20170725T165004__VV_A146_E048N012T6_EU500M_R01_S1BIWG1.tif')

        self.yeoda_fn['version_run_id'] = 'V01R0'
        fn_str = str(self.yeoda_fn)
        self.assertEqual(fn_str, 'SSM_20080101T122333_20090202T220101_____V01R0_.tif')

        self.yeoda_fn['version_run_id'] = ''
        fn_str = str(self.yeoda_fn)
        self.assertEqual(fn_str, 'SSM_20080101T122333_20090202T220101______.tif')

        self.yeoda_fn['version_run_id'] = 'V001R002'
        fn_str = str(self.yeoda_fn)
        self.assertEqual(fn_str, 'SSM_20080101T122333_20090202T220101_____V001R002_.tif')

    def test7_replace_fnparts(self):
        """
        Test all types of fields can be altered after creating the SmartFilename object.

        """
        self.yeoda_fn5['version_run_id'] = 'V01R01'
        self.assertEqual(str(self.yeoda_fn5), 'TMENSIG40_20170725_20181225__A146_E048N012T6_EU500M_V01R01_ASAWS.tif')
        self.assertEqual(self.yeoda_fn5['version_run_id'], 'V01R01')

        self.yeoda_fn5['version_run_id'] = ''
        self.assertEqual(str(self.yeoda_fn5), 'TMENSIG40_20170725_20181225__A146_E048N012T6_EU500M__ASAWS.tif')

        self.yeoda_fn5['band'] = 'VV'
        self.assertEqual(str(self.yeoda_fn5), 'TMENSIG40_20170725_20181225_VV_A146_E048N012T6_EU500M__ASAWS.tif')
        self.assertEqual(self.yeoda_fn5['band'], 'VV')

        self.yeoda_fn5['band'] = ''
        self.assertEqual(str(self.yeoda_fn5), 'TMENSIG40_20170725_20181225__A146_E048N012T6_EU500M__ASAWS.tif')


class TestYeodaPath(unittest.TestCase):
    """
    Tests checking if a yeoda path is correctly reflected by yeoda_tree.
    """

    def setUp(self):
        """
        Setting up the test yeoda_tree.
        """

        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_data', 'Sentinel-1_CSAR_IWGRDH')

    def test_full_path(self):
        """
        Tests the SmartPath() for the yeoda naming conventions
        """

        should = os.path.join(self.test_dir, 'SSM', 'V03R01', 'EQUI7_EU500M', 'E048N012T6', 'qlooks')

        stp1 = yeoda_path(self.test_dir, product='SSM', version=3, run_num=1, grid='EQUI7_EU500M',
                          tile='E048N012T6', qlook=True, make_dir=False)

        self.assertEqual(stp1.directory, should)

        # passing the version as string directly
        stp2 = yeoda_path(self.test_dir, product='SSM', version='V03', run_num=1, grid='EQUI7_EU500M',
                          tile='E048N012T6', qlook=True, make_dir=False)

        self.assertEqual(stp2.directory, should)

    def test_logfile_path(self):
        """
        Test the path for logfiles.

        """

        should = os.path.join(self.test_dir, 'SSM', 'V03R01')
        stp = yeoda_path(self.test_dir, datalog='logfiles', product='SSM', version=3, run_num=1, grid='EQUI7_EU500M',
                          tile='E048N012T6', qlook=True, make_dir=False)
        self.assertEqual(stp.directory, should)


class TestYeodaTree(unittest.TestCase):
    """
    Tests checking if a yeoda tree is correctly reflected by yeoda_tree.
    """

    def setUp(self):
        """
        Setting up the test yeoda_tree.
        """

        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_data', 'Sentinel-1_CSAR_IWGRDH')
        self.hierarchy_should = ['root', 'product', 'wflow', 'grid', 'tile', 'qlook']
        self.stt = yeoda_tree(self.test_dir, register_file_pattern='.tif')


    def test_tree_hierarchy(self):
        """
        Tests if a correct yeoda hierarchy was built.
        """

        self.assertEqual(self.stt.hierarchy, self.hierarchy_should)

        self.assertEqual(self.stt.root, self.test_dir)


    def test_tree_depth(self):
        """
        Checks if maximum depth is not violated.
        """

        max_depth_allowed = len(self.stt.root.split(os.sep)) + \
                            len(self.hierarchy_should) - 1

        self.assertTrue(all([len(x.split(os.sep)) <= max_depth_allowed
                             for x in self.stt.get_all_dirs()]))


if __name__ == "__main__":
    unittest.main()
