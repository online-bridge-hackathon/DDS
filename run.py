from dds import DDS


def dds_scores(dds, state, target, solutions, mode=1):
    n = len(state['plays']) % 4
    first = state['plays'][-n][0] if n > 0 else state['turn']
    trick = [c for _, c in state['plays'][-n:]] if n > 0 else []
    return dds.solve_board(state['trump'], first, trick, state['hands'], target, solutions, mode)


if __name__ == "__main__":
    dds = DDS(max_threads=2)
    state = {
        'plays': [['W', 'H8']],
        'hands': {
            'S': ['D3', 'C6', 'DT', 'D8', 'DJ', 'D6', 'CA', 'C3', 'S2', 'C2', 'C4', 'S9', 'S7'],
            'W': ['DA', 'S4', 'HT', 'C5', 'D4', 'D7', 'S6', 'S3', 'DK', 'CT', 'D2', 'SK'],
            'N': ['C7', 'H6', 'H7', 'H9', 'CJ', 'SA', 'S8', 'SQ', 'D5', 'S5', 'HK', 'C8', 'HA'],
            'E': ['H2', 'H5', 'CQ', 'D9', 'H4', 'ST', 'HQ', 'SJ', 'HJ', 'DQ', 'H3', 'C9', 'CK']
        },
        'trump': 'N'
    }
    # Solve for a specific position inside the play
    # print(dds_scores(dds, state, target=-1, solutions=3))

    # Generate the table at the end of the board
    state['hands']['W'].append('H8')
    print(dds.calc_dd_table(state['hands']))

