import unittest

import numpy as np

from stonehenge.chronology_crosscheck import (
    analyze, calibrate, hpd, load_curve, load_dates, round_out, to_bc, ward_wilson,
)


class TestCalibration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curve = load_curve()

    def test_calendar_convention(self):
        self.assertEqual(int(to_bc(1950)), 1)
        self.assertEqual(int(to_bc(4500)), 2551)

    def test_pdf_normalised_and_hpd_mass(self):
        grid, pdf = calibrate(4023, 21, self.curve)
        self.assertAlmostEqual(pdf.sum(), 1.0, places=9)
        self.assertAlmostEqual(sum(p for _, _, p in hpd(grid, pdf)), 0.954, delta=0.002)

    def test_reproduces_willis_2016_burial_007(self):
        # Willis et al. 2016 Table 2: 4366±25 BP, T'=4.6, 3090-2900 cal BC (IntCal13)
        t = ward_wilson([4420, 4317], [35, 33])
        self.assertAlmostEqual(t['weighted_mean_bp'], 4366, delta=1)
        self.assertAlmostEqual(t['T'], 4.6, delta=0.05)
        ranges = round_out(hpd(*calibrate(t['weighted_mean_bp'], t['err'], self.curve)))
        self.assertAlmostEqual(ranges[0][0], 3090, delta=20)
        self.assertAlmostEqual(ranges[-1][1], 2900, delta=20)

    def test_published_ranges_agree_within_curve_revision(self):
        # Older curves (pre-1998 and IntCal13) differ from IntCal20 in places, so test agreement
        # in aggregate; individual shifts are documented in docs/CHRONOLOGY_CROSSCHECK.md.
        diffs = []
        for d in load_dates().values():
            if not d['published_cal_bc_95']:
                continue
            old, young = map(int, d['published_cal_bc_95'].split('-'))
            r = round_out(hpd(*calibrate(d['bp'], d['err'], self.curve)))
            diffs += [abs(r[0][0] - old), abs(r[-1][1] - young)]
        self.assertLessEqual(np.median(diffs), 10)
        self.assertGreater(np.mean(np.array(diffs) <= 25), 0.75)

    def test_round_out_merges_touching_ranges(self):
        self.assertEqual(round_out([(2621, 2614, 0.4), (2613, 2611, 0.2)]), [(2625, 2610, 0.6000000000000001)])


class TestChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checks = analyze()['checks']

    def test_y30_antlers_not_one_event(self):
        self.assertFalse(self.checks['y_hole_30_antlers']['ward_wilson']['consistent'])

    def test_sarsen_pair_consistent_but_gap_wide(self):
        c = self.checks['sarsen_construction_two_dates']
        self.assertTrue(c['ward_wilson']['consistent'])
        lo, hi = c['gap_trilithon_minus_circle']['ci95_years']
        self.assertGreater(hi - lo, 200)

    def test_aubrey_hole_predates_sarsen(self):
        self.assertGreater(self.checks['aubrey_hole_to_sarsen_gap']['gap_years']['ci95_years'][0], 250)


if __name__ == '__main__':
    unittest.main()
