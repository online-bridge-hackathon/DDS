# Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
#
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

# To run the tests from the command line:
# cd DDS
# python3 -m unittest discover

import unittest

from src.dds import DDS

class TestDDS(unittest.TestCase):

    def test_dds_scores(self):
        """
        Manually tests DDS output for the following deal:

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

        TODO:   Check the entire returned JSON object.
                Add more test deals.
                Test for different values of max_threads.
                Test for invalid input, e.g. too many cards, too few, duplicated card
                Tweak input by exchanging an A and a K, make sure output changes to match.
        """
        
        hands = {
                 "S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],
                 "W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK", "H8"],
                 "N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],
                 "E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]
                }

        dds = DDS()
        dds_table = dds.calc_dd_table(hands)

        self.assertEqual(8, dds_table['C']['S'], 'South can take 8 tricks with clubs as trump')
        self.assertEqual(6, dds_table['N']['E'], 'East can take 6 tricks at notrump')

if __name__ == '__main__':
    unittest.main()
