# Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
#
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

# TODO: Add support for the similar format that the dds C++ library uses for
#       its test deals. Those are easier to enter but a little more difficult
#       to read.

from threading import Thread

SUIT_SYMBOLS = ["S", "H", "D", "C"]

def string_to_hand(hand_string):
    # Input string example: "AQ85.AK976.5.J87"

    # Output dict: ['SA', 'SQ', 'S8', 'S5', 'HA', 'HK', 'H9', 'H7', 'H6', 'D5', 'CJ', 'C8', 'C7']

    suits = hand_string.split('.')

    hand = []
    for index in range(4):
        suit_symbol = SUIT_SYMBOLS[index]

        # The holding in a single suit, e.g., "AQ85"
        holding = suits[index]

        for card in holding:
            hand.append(suit_symbol + card)

    return hand

def nesw_to_dds_format(nesw):
    # Input:
    # A list of four strings representing four bridge hands, in order North,
    # East, South, and Eest, with the suits separated by periods, e.g.
    # [
    #    "AQ85.AK976.5.J87",
    #    "JT.QJ5432.Q9.KQ9",
    #    "972..JT863.A6432",
    #    "K643.T8.AK742.T5"
    # ]
    #
    # Output:
    # A Python dictionary with the entries expected by dds.calc_dd_table(), e.g.,
    # {
    #    "N": ['SA', 'SQ', 'S8', 'S5', 'HA', 'HK', 'H9', 'H7', 'H6', 'D5', 'CJ', 'C8', 'C7']
    #    "E": ['SJ', 'ST', 'HQ', 'HJ', 'H5', 'H4', 'H3', 'H2', 'DQ', 'D9', 'CK', 'CQ', 'C9']
    #    "S": ['S9', 'S7', 'S2', 'DJ', 'DT', 'D8', 'D6', 'D3', 'CA', 'C6', 'C4', 'C3', 'C2']
    #    "W": ['SK', 'S6', 'S4', 'S3', 'HT', 'H8', 'DA', 'DK', 'D7', 'D4', 'D2', 'CT', 'C5']
    # }

    # This could be written as a loop, but the code would be harder to follow
    return {
        "N": string_to_hand(nesw[0]),
        "E": string_to_hand(nesw[1]),
        "S": string_to_hand(nesw[2]),
        "W": string_to_hand(nesw[3])
    }

def rotate_nesw_to_eswn(nesw):
    eswn = []
    for index in range(4):
        eswn.append(nesw[(index + 1) %4])
    return eswn

def run_in_threads(num_threads, target, args):
    """
    Helper to run a test using multiple threads with a simulated return value
    """
    results = []
    threads = []
    # Wrapper to allow thread functions to return or yield their return values
    def thread_fn(target, args, result):
        for r in target(*args):
            result.append(r)
    for i in range(num_threads):
        # Reserve a thread local return value
        results.append([])
        thread_arguments = (target, args, results[i])
        # Create and start threads
        threads.append(Thread(target=thread_fn, args=thread_arguments))
        threads[i].start()


    for t in threads:
        # Wait for thread exit
        t.join()

    # collapse results to a single list
    for thread_return in results:
        for item in thread_return:
            yield item
