# Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
#
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

# To run the tests from the command line:
# cd DDS
# python3 -m unittest discover

import unittest
import threading

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

    def setUp(self):
        # We do this here rather than in setUpClass() in order to test
        # multiple serial instantiations of DDS. At one point DDS had
        # a bug that caused it to crash when we did this.
        self.dds = DDS()

    def test_one_sample_deal(self):
        """
        Solve a sample.
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
        NS make 13 tricks in everything.
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
        Everyone makes 9 tricks in notrump!
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

    def skip_test_one_trick_deal(self):
        """
        This test fails. Presumably we have not yet implemented deals of
        fewer than 52 cards.

            S A
            H 
            D 
            C 

        S       
        H           A
        D      
        C A         

            S 
            H
            D A
            C 
        """

        nesw = [
            "A...",
            ".A..",
            "..A.",
            "...A"
        ]

        hands = nesw_to_dds_format(nesw)

        dds_table = self.dds.calc_dd_table(hands)

        self.assertEqual(0, dds_table['S']['N'], 'South can take no tricks at notrump')
        self.assertEqual(1, dds_table['S']['N'], 'South can take one tricks at diamonds')

    def test_parallel_CalcDDTable(self):
        """
        Tests parallel access to dds.calc_dd_table.
        Cards are from libdds/hands/list100.txt

        PBN 0 0 4 2 "N:T742.QT6.AJ7.Q64 AQ83.A54.KQ9.T82 K65.J873.653.A97 J9.K92.T842.KJ53"
        FUT 10 3 2 2 1 1 1 3 3 0 0 14 3 6 3 8 11 7 9 6 13 0 0 32 0 128 0 0 0 32 0 5 5 5 5 5 5 5 5 4 4
        TABLE 5 8 5 8  6 7 6 7  4 8 4 8  4 8 4 8  5 8 5 8
        """

        nesw = [
            "T742.QT6.AJ7.Q64",
            "AQ83.A54.KQ9.T82",
            "K65.J873.653.A97",
            "J9.K92.T842.KJ53"
        ]

        result = dict(
            S = dict(N = 5, E = 8, S = 5, W = 8),
            H = dict(N = 6, E = 7, S = 6, W = 7),
            D = dict(N = 4, E = 8, S = 4, W = 8),
            C = dict(N = 4, E = 8, S = 4, W = 8),
            N = dict(N = 5, E = 8, S = 5, W = 8)
        )

        deal = nesw_to_dds_format(nesw)

        def test_fn(self, deal, solutions):
            for i in range(2):
                solutions.append(self.dds.calc_dd_table(deal))

        solutions = []
        solutions2 = []

        t2 = threading.Thread(target=test_fn, args=(self, deal, solutions2))
        t2.start()
        test_fn(self, deal, solutions)
        t2.join()
        solutions.extend(solutions2)

        for solution in solutions:
            for denomination in ['C', 'D', 'H', 'S', 'N']:
                for declarer in ['N', 'S', 'E', 'W']:
                    self.assertEqual(result[denomination][declarer],
                            solution[denomination][declarer],
                            declarer + ' should make ' + \
                                    str(result[denomination][declarer]) + ' in ' + \
                                    denomination);


if __name__ == '__main__':
    unittest.main()
