# rdate: Alternative to standard datetime library.
# Copyright: (c) 2018, t5w5h5@gmail.com. All rights reserved.
# License: MIT, see LICENSE for details.

import unittest

from rdate import *


class TestEnums(unittest.TestCase):

    def test_period(self):
        self.assertTrue(Period.Week == Period.Week)
        self.assertTrue(Period.Week < Period.Month)
        self.assertFalse(Period.Week > Period.Month)
        self.assertFalse(Period.Week == Period.Month)
        period = list(Period)
        for p in range(len(period)-1):
            self.assertTrue(period[p] < period[p+1])

    def _test_weekday(self, first_day=None):
        if first_day is not None:
            set_first_day_of_week(first_day)

        self.assertEqual(Weekday.first_day_of_week(), Weekday.Monday if first_day is None else first_day)

        # Addition
        self.assertEqual(Weekday.Monday+1, Weekday.Tuesday)
        self.assertEqual(Weekday.Monday+7, Weekday.Monday)
        self.assertEqual(Weekday.Monday+8, Weekday.Tuesday)

        # Subtraction
        self.assertEqual(Weekday.Monday-1, Weekday.Sunday)
        self.assertEqual(Weekday.Monday-7, Weekday.Monday)
        self.assertEqual(Weekday.Monday-8, Weekday.Sunday)

        # Difference
        self.assertEqual(Weekday.Sunday - Weekday.Sunday, 0)
        self.assertEqual(Weekday.Sunday - Weekday.Monday, 6)
        self.assertEqual(Weekday.Monday - Weekday.Sunday, -6)

        # Comparisons
        self.assertTrue(Weekday.Monday == Weekday.Monday)
        self.assertTrue(Weekday.Monday < Weekday.Friday)
        self.assertFalse(Weekday.Monday > Weekday.Friday)
        self.assertFalse(Weekday.Monday == Weekday.Friday)
        wds = Weekday.range()
        for d in range(len(wds)-1):
            self.assertTrue(wds[d] < wds[d+1])

    def test_weekday(self):
        self._test_weekday()
        self._test_weekday(Weekday.Sunday)


class TestTime(unittest.TestCase):

    def test_now(self):
        t1 = t2 = Time.now()
        self.assertEqual(t1, t2)

    def test_init(self):
        with self.assertRaisesRegex(ValueError, "Invalid hour: 24"):
            Time(24, 0, 0)

        with self.assertRaisesRegex(ValueError, "Invalid time: 2.0"):
            Time(2.0)

        with self.assertRaisesRegex(ValueError, "Invalid time: invalid"):
            Time('invalid')

        with self.assertRaisesRegex(ValueError, "Invalid time: 123:10:00"):
            Time('123:10:00')

        # from ints
        self.assertEqual(Time(12, 10, 1), Time(12, 10, 1))

        # from str
        self.assertEqual(Time('12:10:00'), Time(12, 10))
        self.assertEqual(Time('12:1'), Time(12, 1))
        self.assertEqual(Time('1:19'), Time(1, 19))

        # from Time
        t = Time.now()
        self.assertEqual(Time(t), t)

    def test_str(self):
        self.assertEqual(str(Time(13)), '13:00:00')
        self.assertEqual(str(Time(0, 10, 20)), '00:10:20')

    def test_diff(self):
        self.assertEqual(Time(12).diff(Time(13, 0, 0)), 3600)
        self.assertEqual(Time(0).diff(Time(23, 59, 59)), 86399)
        self.assertEqual(Time.end_of_day().diff(Time.start_of_day()), -86399)

    def test_comparisons(self):
        self.assertTrue(Time(12) == Time(12))
        self.assertTrue(Time(12) <= Time(12))

        self.assertTrue(Time(12) < Time(12, 0, 1))
        self.assertTrue(Time(12) <= Time(12, 0, 1))

        self.assertFalse(Time(12, 0, 1) < Time(12))
        self.assertTrue(Time(12, 0, 1) > Time(12))
        self.assertTrue(Time(12, 0, 1) >= Time(12))

        self.assertTrue(Time(12, 0, 1) != Time(12))


class TestDate(unittest.TestCase):

    def test_today(self):
        d = Date.today()
        self.assertEqual(d, d.next().prev())

    def test_init(self):
        with self.assertRaisesRegex(ValueError, "Invalid month: 13"):
            Date(2015, 13, 1)

        with self.assertRaisesRegex(ValueError, "Invalid date: invalid"):
            Date('invalid')

        with self.assertRaisesRegex(ValueError, "Invalid date: 10-01-01"):
            Date('10-01-01')

        with self.assertRaisesRegex(ValueError, "Invalid date: 1.0"):
            Date(1.0)

        # from ints
        self.assertEqual(Date(2014, 12, 31), Date(2014, 12, 31))

        # from str
        self.assertEqual(Date('2010-11-12'), Date(2010, 11, 12))
        self.assertEqual(Date('2010-1-1'), Date(2010, 1, 1))

        # from Date
        d = Date.today()
        self.assertEqual(Date(d), d)

    def test_comparisons(self):
        d = Date.today()

        self.assertEqual(d, d.next().prev())
        self.assertEqual(d, d.next(1, Period.Week).prev(1, Period.Week))
        self.assertEqual(d, d.next(1, Period.Month).prev(1, Period.Month))
        self.assertEqual(d, d.next(1, Period.Year).prev(1, Period.Year))
        self.assertEqual(d, d.next().prev())
        self.assertNotEqual(d, d.next())
        self.assertNotEqual(d, d.prev())

        self.assertLess(d, d.next())
        self.assertLessEqual(d, d.next())
        self.assertLessEqual(d, d)

        self.assertGreater(d, d.prev())
        self.assertGreaterEqual(d, d.prev())
        self.assertGreaterEqual(d, d)

    def test_next(self):
        d = Date(2015, 1, 1)
        self.assertEqual(d.next(), Date(2015, 1, 2))
        self.assertEqual(d.next(44), Date(2015, 2, 14))
        self.assertEqual(d.next(0), d)

    def test_prev(self):
        d = Date(2015, 1, 1)

        self.assertEqual(d.prev(), Date(2014, 12, 31))
        self.assertEqual(d.prev(44), Date(2014, 11, 18))
        self.assertEqual(d.prev(0), d)

        self.assertEqual(d.prev(1, Period.Month), Date(2014, 12, 1))
        self.assertEqual(d.prev(2, Period.Month), Date(2014, 11, 1))

        self.assertEqual(Date(2014, 12, 31).prev(1, Period.Month), Date(2014, 11, 30))
        self.assertEqual(Date(2014, 2, 28).prev(1, Period.Month), Date(2014, 1, 28))

    def test_envelope(self):
        d = Date(2015, 6, 2)

        ds, de = d.envelope(Period.Day)
        self.assertEqual(ds, d)
        self.assertEqual(de, ds)

        ds, de = d.envelope(Period.Day, Date(2015, 6, 5))
        self.assertEqual(ds, d)
        self.assertEqual(de, Date(2015, 6, 5))

        with self.assertRaises(ValueError):
            ds, de = d.envelope(Period.Day, Date(2015, 6, 1))

        ws, we = d.envelope()
        self.assertEqual(ws, Date(2015, 6, 1))
        self.assertEqual(we, Date(2015, 6, 7))

        ms, me = d.envelope(Period.Month)
        self.assertEqual(ms, Date(2015, 6, 1))
        self.assertEqual(me, Date(2015, 6, 30))

        ys, ye = d.envelope(Period.Year)
        self.assertEqual(ys, Date(2015, 1, 1))
        self.assertEqual(ye, Date(2015, 12, 31))

        ws, we = d.envelope(to_date=Date(2015, 7, 2))
        self.assertEqual(ws, Date(2015, 6, 1))
        self.assertEqual(we, Date(2015, 7, 5))

        ws, we = Date(2015, 6, 1).envelope(to_date=Date(2015, 7, 5))
        self.assertEqual(ws, Date(2015, 6, 1))
        self.assertEqual(we, Date(2015, 7, 5))

    def test_diff(self):
        self.assertEqual(Date(2015, 6, 1).diff(Date(2015, 6, 1)), 0)
        self.assertEqual(Date(2015, 6, 1).diff(Date(2015, 6, 2)), 1)
        self.assertEqual(Date(2015, 6, 2).diff(Date(2015, 6, 1)), -1)

        self.assertEqual(Date(2015, 6, 2).diff(Date(2015, 6, 7), Period.Week), 0)
        self.assertEqual(Date(2015, 6, 2).diff(Date(2015, 6, 8), Period.Week), 1)
        self.assertEqual(Date(2015, 6, 2).diff(Date(2015, 5, 28), Period.Week), -1)

        self.assertEqual(Date(2015, 6, 20).diff(Date(2015, 6, 7), Period.Month), 0)
        self.assertEqual(Date(2015, 6, 20).diff(Date(2015, 7, 1), Period.Month), 1)
        self.assertEqual(Date(2015, 6, 20).diff(Date(2015, 5, 1), Period.Month), -1)
        self.assertEqual(Date(2015, 6).diff(Date(2014, 5), Period.Month), -13)

        self.assertEqual(Date(2015, 1, 1).diff(Date(2015, 12, 31), Period.Year), 0)
        self.assertEqual(Date(2015, 6, 20).diff(Date(2016, 7, 1), Period.Year), 1)
        self.assertEqual(Date(2015, 6, 20).diff(Date(2014, 5, 1), Period.Year), -1)
        self.assertEqual(Date(2010).diff(Date(2014), Period.Year), 4)

    def test_length(self):
        self.assertEqual(Date(2015, 6, 6).length(), 30)
        self.assertEqual(Date(2012, 2, 6).length(), 29)
        self.assertEqual(Date(2013, 2, 6).length(period=Period.Year), 365)
        self.assertEqual(Date(2012, 2, 6).length(period=Period.Year), 366)

    def test_range(self):
        self.assertEqual(Date(2015, 2, 1).range(n=0)[0], Date(2015, 2, 1))
        self.assertEqual(Date(2015, 2, 1).range(Date(2015, 2, 1))[0], Date(2015, 2, 1))

        self.assertEqual(len(Date(2015, 2, 1).range(n=0)), 1)
        self.assertEqual(len(Date(2015, 2, 1).range(n=1)), 2)
        self.assertEqual(len(Date(2015, 2, 1).range(n=-1)), 2)
        self.assertEqual(Date(2015, 2, 1).range(n=1)[1], Date(2015, 2, 2))
        self.assertEqual(Date(2015, 2, 1).range(n=-1)[1], Date(2015, 1, 31))

        self.assertEqual(len(Date(2015, 2, 1).range(Date(2015, 2, 1))), 1)
        self.assertEqual(len(Date(2015, 2, 1).range(Date(2015, 2, 2))), 2)
        self.assertEqual(len(Date(2015, 2, 1).range(Date(2015, 1, 31))), 2)
        self.assertEqual(Date(2015, 2, 1).range(Date(2015, 2, 2))[1], Date(2015, 2, 2))
        self.assertEqual(Date(2015, 2, 1).range(Date(2015, 1, 31))[1], Date(2015, 1, 31))

    def test_attr(self):
        d = Date(2015, 6, 2)
        self.assertEqual(d.year, 2015)
        self.assertEqual(d.month, 6)
        self.assertEqual(d.day, 2)
        self.assertEqual(d.weekday, Weekday.Tuesday)

    def test_istoday(self):
        self.assertTrue(Date.today().istoday)
        self.assertFalse(Date.today().next().istoday)
        self.assertFalse(Date(2014, 1, 1).istoday)

    def test_isweekend(self):
        self.assertFalse(Date(2015, 6, 5).isweekend)
        self.assertTrue(Date(2015, 6, 6).isweekend)
        self.assertTrue(Date(2015, 6, 7).isweekend)
        self.assertFalse(Date(2015, 6, 8).isweekend)

    def test_isleap(self):
        self.assertFalse(Date(2013, 2, 6).isleap)
        self.assertTrue(Date(2012, 2, 6).isleap)

    def test_equal(self):
        d1 = Date('2015-05-17')
        d2 = Date('2015-05-17')
        self.assertEqual(d1, d2)
        self.assertFalse(d1 == None)

    def test_find_day(self):
        with self.assertRaises(ValueError):
            Date.find_day(2015, 2, Weekday.Sunday, 10)

        with self.assertRaises(ValueError):
            Date.find_day(2015, 2, Weekday.Sunday, 5)

        self.assertEqual(Date.find_day(2015, 3, Weekday.Sunday, 1), Date(2015, 3, 1))
        self.assertEqual(Date.find_day(2015, 3, Weekday.Sunday, 2), Date(2015, 3, 8))
        self.assertEqual(Date.find_day(2015, 3, Weekday.Tuesday, 5), Date(2015, 3, 31))


class TestDateTime(unittest.TestCase):

    def test_now(self):
        dt = DateTime.now()
        self.assertEqual(dt.date, Date.today())
        self.assertEqual(dt.time, Time.now())

    def test_create(self):
        with self.assertRaisesRegex(ValueError, "Invalid date/time: 1.0"):
            DateTime(1.0)

        with self.assertRaisesRegex(ValueError, "Invalid date/time: 2015-05-17-15:33:26"):
            DateTime('2015-05-17-15:33:26')

        with self.assertRaisesRegex(ValueError, "Invalid date/time: 15-05-17 15:33:26"):
            DateTime('15-05-17 15:33:26')

        # from str
        dt = DateTime('2015-3-11 0:0')
        self.assertEqual(dt.date, Date(2015, 3, 11))
        self.assertEqual(dt.time, Time(0, 0))

        dt = DateTime('2015-05-17,15:33:26')
        self.assertEqual(dt.date, Date(2015, 5, 17))
        self.assertEqual(dt.time, Time(15, 33, 26))

        # from DateTime
        dt = DateTime('2015-05-17,15:33:26')
        self.assertEqual(DateTime(dt), dt)

    def test_str(self):
        self.assertEqual(str(DateTime((Date(2015, 3, 5), Time(14, 22)))), '2015-03-05 14:22:00 EST')
        self.assertEqual(DateTime((Date(2015, 3, 5), Time(14, 22))).isostr(), '2015-03-05T14:22:00.000000-05:00')
        self.assertEqual(DateTime((Date(2015, 3, 15), Time(14, 22))).isostr(), '2015-03-15T14:22:00.000000-04:00')

    def test_diff(self):
        self.assertEqual(DateTime((Date(2015, 2, 1), Time(9, 30))).diff(DateTime((Date(2015, 2, 2), Time(9, 30)))), 86400)

    def test_since(self):
        self.assertEqual(DateTime.now().since(), 0)

    def test_to(self):
        self.assertEqual(DateTime('2015-05-17 15:33:26').to(36001), DateTime('2015-05-18 1:33:27'))
        self.assertEqual(DateTime('2015-05-17 15:33:26').to(-36001), DateTime('2015-05-17 5:33:25'))

    def test_equal(self):
        dt1 = DateTime('2015-05-17 15:33:26')
        dt2 = DateTime('2015-05-17 15:33:26')
        self.assertEqual(dt1, dt2)
        self.assertFalse(dt1 is None)

    def test_comparisons(self):
        dt1 = DateTime('2015-05-17 15:33:26')
        dt2 = DateTime('2015-05-17 15:33:27')
        self.assertNotEqual(dt1, dt2)
        self.assertTrue(dt1 < dt2)
        self.assertTrue(dt1 <= dt2)
        self.assertFalse(dt1 > dt2)
        self.assertFalse(dt1 >= dt2)


class TestTimestamp(unittest.TestCase):

    def test_datetime(self):
        dt = DateTime((Date(2015, 3, 5), Time(14, 22)))
        ts = timestamp(dt)
        self.assertEqual(DateTime(ts), dt)

    def test_current(self):
        self.assertGreater(timestamp(prec=0.01), timestamp(prec=0.1))

        dt = DateTime.now()
        self.assertEqual(timestamp(prec=1.0), timestamp(dt))
        self.assertGreater(timestamp(), timestamp(dt))

        t1 = timestamp(prec=0.0001)
        t2 = timestamp(prec=0.0001)
        self.assertEqual(t2, t1)

        t1 = timestamp(prec=0.000001)
        t2 = timestamp(prec=0.000001)
        self.assertGreater(t2, t1)
