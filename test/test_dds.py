# Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
#
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

# To run the tests from the command line:
# cd DDS
# python3 -m unittest discover

import unittest

from test.utilities import nesw_to_dds_format
from test.utilities import rotate_nesw_to_eswn

from src.dds import DDS

# So we can use multi-line strongs as comments:
# pylint: disable=pointless-string-statement

class TestDDS(unittest.TestCase):
    """
    Tests DDS output for a few specific deals.

    TODO:   Test for different values of max_threads.
            Test for invalid input, e.g. too many cards, too few, duplicated card.
            Tweak input by exchanging an A and a K, make sure output changes to match.
    """

    @classmethod
    def setUpClass(cls):
        # Cannot use setUp() because we are only able to instantiate DDS once.
        # This is likely a bug in DDS…
        cls.dds = DDS()

    def test_one_sample_deal(self):
        """
            S AQ85
            H AK976
            D 5
            C J87

        S K643      JT
        H T8        QJ5432
        D AK742     Q9
        C T5        KQ9

            S 972
            H
            D JT863
            C A6432
        """

        nesw = [
            "AQ85.AK976.5.J87",
            "JT.QJ5432.Q9.KQ9",
            "972..JT863.A6432",
            "K643.T8.AK742.T5"
        ]

        hands = nesw_to_dds_format(nesw)

        dds_table = self.dds.calc_dd_table(hands)

        self.assertEqual(8, dds_table['C']['S'], 'South can take 8 tricks with clubs as trump')
        self.assertEqual(6, dds_table['N']['E'], 'East can take 6 tricks at notrump')

    def test_ns_make_7_of_everything(self):
        """
            S AKQJ
            H AKQJ
            D T98
            C T9

        S 76        5432
        H 876       5432
        D 7654      32
        C 8765      432

            S T98
            H T9
            D AKQJ
            C AKQJ
        """

        nesw = [
            "AKQJ.AKQJ.T98.T9",
            "5432.5432.32.432",
            "T98.T9.AKQJ.AKQJ",
            "76.876.7654.8765"
        ]

        hands = nesw_to_dds_format(nesw)

        dds_table = self.dds.calc_dd_table(hands)

        for denomination in ['C', 'D', 'H', 'S', 'N']:
            for declarer in ['N', 'S']:
                self.assertEqual(13, dds_table[denomination][declarer],
                                 "NS can take 13 tricks in any denomination.")
            for declarer in ['E', 'W']:
                self.assertEqual(0, dds_table[denomination][declarer],
                                 "EW can take 0 tricks in any denomination.")

        # Now test the same deal, but rotated 90 degrees clockwise

        nesw = rotate_nesw_to_eswn(nesw)

        hands = nesw_to_dds_format(nesw)

        dds_table = self.dds.calc_dd_table(hands)

        for denomination in ['C', 'D', 'H', 'S', 'N']:
            for declarer in ['N', 'S']:
                self.assertEqual(0, dds_table[denomination][declarer],
                                 "NS can take 0 tricks in any denomination.")
            for declarer in ['E', 'W']:
                self.assertEqual(13, dds_table[denomination][declarer],
                                 "EW can take 13 tricks in any denomination.")
        
    def test_everyone_makes_3n(self):
        """
        Unusual deal!
        See: https://bridge.thomasoandrews.com/deals/everybody/

            S QT9
            H A8765432
            D KJ
            C -

        S -         KJ
        H KJ        -
        D QT9       A8765432
        C A8765432  QT9

            S A8765432
            H QT9
            D -
            C KJ
        """

        nesw = [
            "QT9.A8765432.KJ.",
            "KJ..A8765432.QT9",
            "A8765432.QT9..KJ",
            ".KJ.QT9.A8765432"
        ]

        hands = nesw_to_dds_format(nesw)

        dds_table = self.dds.calc_dd_table(hands)

        for declarer in ['N', 'E', 'S', 'W']:
            self.assertEqual(9, dds_table['N'][declarer],
                             "Every declarer can take 9 tricks at NT.")

if __name__ == '__main__':
    unittest.main()
