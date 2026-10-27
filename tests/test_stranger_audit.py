import unittest

from stonehenge.stranger_audit import (
    analyze, cyclic_code_min_distance, obliquity_deg, refraction_deg, rise_azimuth, station_angle,
    LATITUDE, SUN_SEMIDIAMETER,
)


class TestMath(unittest.TestCase):
    def test_obliquity_j2000_and_trend(self):
        self.assertAlmostEqual(obliquity_deg(2000), 23.43929, places=4)
        self.assertGreater(obliquity_deg(-2499), obliquity_deg(2000))

    def test_refraction_at_horizon(self):
        self.assertAlmostEqual(refraction_deg(0.0), 0.57, delta=0.02)

    def test_equinox_rises_due_east_geometrically(self):
        self.assertAlmostEqual(float(rise_azimuth(0.0, LATITUDE, 0.0, SUN_SEMIDIAMETER, physical=False)), 90.0, places=9)

    def test_station_angle_simple_geometry(self):
        # hand check: arccos(-sin 29.119/cos phi) - arccos(sin 23.974/cos phi) at phi = 51.179
        self.assertAlmostEqual(float(station_angle(LATITUDE, obliquity_deg(-2499), 0.0, physical=False)), 91.3, delta=0.1)

    def test_cyclic_code_distance_known_case(self):
        # length-7 simplex code (check polynomial x^3+x+1) has minimum distance 4
        self.assertEqual(cyclic_code_min_distance(0b1011, n=7), 4)


class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = analyze()

    def test_repo_code_claim_refuted(self):
        c = self.r['aubrey_code']
        self.assertTrue(c['x7_plus_1_divisible_by_g'])
        self.assertNotEqual(c['d_min_if_g_is_check_polynomial'], 18)

    def test_strangers_test_does_not_pass(self):
        self.assertFalse(self.r['strangers_test']['returns'])
        self.assertGreaterEqual(self.r['strangers_test']['tally']['FAIL'], 1)

    def test_look_elsewhere_exceeds_repo_p(self):
        self.assertGreater(self.r['sacred_rod_look_elsewhere']['random_rod_0.5_to_2m']['1-9 x 10^n']['p_match_as_good'], 0.0002)

    def test_speech_inaudible_at_durrington(self):
        self.assertLess(self.r['acoustic_exclusion']['speech_60dB_at_1m_heard_at_2500m_dB_SPL'], 0)

    def test_leap_hole_rule_is_sound(self):
        self.assertLess(abs(self.r['arithmetic']['leap_hole_rule']['residual_after_1100_years_holes']), 0.5)


if __name__ == '__main__':
    unittest.main()
