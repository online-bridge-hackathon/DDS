# Copyright 2020 Pauli Nieminen and the Bridge Hackathon contributors
#
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

# To run the tests from the command line:
# cd DDS
# python3 -m unittest discover

import unittest
import sys
import json

# import dds in api.py requires appending path manually
sys.path.append('src')

from api import app

from test.utilities import string_to_hand
from test.utilities import run_in_threads
from test.utilities import check_DD_table_results

class TestAPI(unittest.TestCase):
    """
    Tests the server handler implementations.
    """

    @classmethod
    def setUp(self):
        self.service = app.test_client()

    def test_parallel_post(self):
        """
        Tests parallel access to calcDDTable. Cards are from libdds/hands/list100.txt
        PBN 0 2 0 3 "N:KT.6.AKQ64.A7654 Q53.KT9874.T2.Q2 AJ876.A2.953.KJT 942.QJ53.J87.983"
        FUT 10 1 1 1 0 0 2 2 0 3 3 3 5 12 2 4 8 11 9 3 9 0 0 2048 0 0 128 0 0 0 256 0 0 0 0 0 0 0 0 0 0
        TABLE 13 0 13 0 8 5 8 5 13 0 13 0 13 0 13 0 13 0 13 0
        """

        deal = dict(
            hands = dict(
                N = string_to_hand("KT.6.AKQ64.A7654"),
                E = string_to_hand("Q53.KT9874.T2.Q2"),
                S = string_to_hand("AJ876.A2.953.KJT"),
                W = string_to_hand("942.QJ53.J87.983")
                )
            )

        result = dict(
            S = dict(N = 13, E = 0, S = 13, W = 0),
            H = dict(N = 8, E = 5, S = 8, W = 5),
            D = dict(N = 13, E = 0, S = 13, W = 0),
            C = dict(N = 13, E = 0, S = 13, W = 0),
            N = dict(N = 13, E = 0, S = 13, W = 0)
        )

        def test_fn(self, deal):
            for i in range(2):
                response = self.service.post('/api/dds-table/', json=deal)
                self.assertEqual(response.status_code, 200)
                yield json.loads(response.data)

        solutions = run_in_threads(2, test_fn, args=(self, deal))

        check_DD_table_results(self, solutions, result)

if __name__ == '__main__':
    unittest.main()
