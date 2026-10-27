import unittest

import numpy as np

from stonehenge.acoustics_precision import (
    air_absorption_db_per_m, analyze, barron_gain_db, cylinder_mode, speed_of_sound,
)


class TestStandards(unittest.TestCase):
    def test_iso_9613_1_reference_values(self):
        # ISO 9613-1:1993 Table 1, 101.325 kPa (dB/km)
        for f, t, rh, expected in [(1000, 20, 70, 4.98), (500, 10, 80, 1.96), (4000, 20, 50, 29.7)]:
            got = air_absorption_db_per_m(f, t, rh, 101.325) * 1000
            self.assertAlmostEqual(got, expected, delta=expected * 0.01)

    def test_speed_of_sound(self):
        self.assertAlmostEqual(float(speed_of_sound(20.0)), 343.2, delta=0.1)
        self.assertAlmostEqual(float(speed_of_sound(0.0)), 331.3, places=6)

    def test_barron_gain_vanishes_without_reflections(self):
        self.assertAlmostEqual(float(barron_gain_db(5.0, 1e-9, 3000.0)), 0.0, places=6)

    def test_quarter_wave_vertical_mode(self):
        self.assertAlmostEqual(cylinder_mode(0, 0, 0, 14.785, 4.9, 333.4), 333.4 / (4 * 4.9), places=9)


class TestAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = analyze(n=20_000)

    def test_reproducible(self):
        self.assertEqual(analyze(n=20_000)['volume_m3'], self.report['volume_m3'])

    def test_114hz_is_not_a_discrete_mode(self):
        self.assertLess(self.report['schroeder_frequency_hz']['ci95'][1], 114.0)
        self.assertGreater(self.report['claim_114hz']['overlapping_modes_in_one_bandwidth']['ci95'][0], 10)

    def test_8hz_wavelength_exceeds_circle(self):
        r = self.report['claim_8_1hz']
        self.assertGreater(r['wavelength_m']['ci95'][0], r['circle_diameter_m']['ci95'][1])

    def test_air_absorption_inaudible_across_circle_below_2khz(self):
        for f in ('8.1Hz', '114Hz', '500Hz', '1000Hz', '2000Hz'):
            self.assertFalse(self.report['air_absorption'][f]['audible_vs_jnd'])

    def test_nodal_drift_sign(self):
        self.assertLess(self.report['aubrey_arithmetic']['drift_per_step_years'], 0)
        self.assertTrue(np.isclose(self.report['aubrey_arithmetic']['three_nodal_periods_years'], 55.84, atol=0.01))


if __name__ == '__main__':
    unittest.main()
