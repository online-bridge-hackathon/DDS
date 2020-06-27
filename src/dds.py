"""See: https://github.com/dds-bridge/dds/blob/develop/doc/dll-description.md"""

from ctypes import Structure, c_int, pointer
import platform

if platform.system() == "Windows":
    from ctypes import windll as libloader
else:
    from ctypes import cdll as libloader

DIRECTIONS = "NESW"
SUITS = "SHDC"
STRAINS = SUITS + "N"
RANKS = "??23456789TJQKA"
MAXNOOFBOARDS = 200

class Deal(Structure):
    _fields_ = [
        ("trump", c_int),
        ("first", c_int),
        ("current_trick_suit", c_int * 3),
        ("current_trick_rank", c_int * 3),
        ("remain_cards", (c_int * 4) * 4)
    ]

class FutureTricks(Structure):
    _fields_ = [
        ("nodes", c_int),
        ("cards", c_int),
        ("suit", c_int * 13),
        ("rank", c_int * 13),
        ("equals", c_int * 13),
        ("score", c_int * 13)
    ]

class DDtable_deal(Structure):
    _fields_ = [
        ("cards", (c_int * 4) * 4)
    ]

class DDTableResults(Structure):
    _fields_ = [
        ("resTable", (c_int * 4) * 5)
    ]

class Boards(Structure):
    _fields_ = [
        ("noOfBoards", c_int),
        ("deals", Deal * MAXNOOFBOARDS),
        ("target", c_int * MAXNOOFBOARDS),
        ("solutions", c_int * MAXNOOFBOARDS),
        ("mode", c_int * MAXNOOFBOARDS)
    ]

class SolvedBoards(Structure):
    _fields_ = [
        ("noOfBoards", c_int),
        ("solvedBoard", FutureTricks * MAXNOOFBOARDS)
    ]

class DDSError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        # This is Python 3.6 string interpolation syntax.
        return f"Error code {self.code}"

def encode_deal(hands):
    cards = ((c_int * 4) * 4)()
    for i, direction in enumerate(DIRECTIONS):
        for card in hands[direction]:
            suit = SUITS.index(card[0])
            rank = RANKS.index(card[1])
            cards[i][suit] |= 1 << rank
    return cards

class DDS:
    def __init__(self, max_threads=0):
        if platform.system() == "Windows":
            libname = "libdds.dll"
        elif platform.system() == "Darwin":
            libname = "libdds.2.dylib"
        else:
            libname = "libdds.so.2"
        self.libdds = libloader.LoadLibrary(libname)
        self.libdds.SetMaxThreads(max_threads)

    def solve_board(self, trump, first, current_trick, hands,
                    target=-1, solutions=3, mode=1, thread_index=0):
        trump = STRAINS.index(trump)
        first = DIRECTIONS.index(first)

        current_trick_suit = (c_int * 3)()
        current_trick_rank = (c_int * 3)()
        for i, card in enumerate(current_trick):
            current_trick_suit[i] = SUITS.index(card[0])
            current_trick_rank[i] = RANKS.index(card[1])

        remain_cards = encode_deal(hands)
        dl = Deal(trump, first, current_trick_suit, current_trick_rank, remain_cards)
        fut = FutureTricks()

        code = self.libdds.SolveBoard(dl, target, solutions, mode, pointer(fut), thread_index)
        if code != 1:
            raise DDSError(code)

        scores = []
        for i in range(fut.cards):
            card = SUITS[fut.suit[i]] + RANKS[fut.rank[i]]
            score = fut.score[i]
            scores.append((card, score))
        return scores

    def calc_dd_table(self, hands):
        cards = encode_deal(hands)
        table_deal = DDtable_deal(cards)
        table = DDTableResults()

        code = self.libdds.CalcDDtable(table_deal, pointer(table))
        if code != 1:
            raise DDSError(code)

        results = dict()
        for strain, row in zip(STRAINS, table.resTable):
            results[strain] = dict(zip(DIRECTIONS, row))
        return results
