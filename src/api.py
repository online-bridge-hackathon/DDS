from flask import Flask, request
from flask_restful import Resource, Api

from dds import DDS

app = Flask(__name__)
api = Api(app)


class DDSTable(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        """Takes in a single hand and returns a DDS table"""
        data = request.get_json()
        # Verify the data here
        # self.verifyinput(data)
        dds = DDS(max_threads=2)
        dds_table = dds.calc_dd_table(data['hands'])
        return dds_table 

class DDSScore(Resource):
    def post(self):
        """This should hook in to the dds_scores function listed below"""
        raise NotImplementedError()

    def dds_scores(dds, state, target, solutions, mode=1):
        n = len(state['plays']) % 4
        first = state['plays'][-n][0] if n > 0 else state['turn']
        trick = [c for _, c in state['plays'][-n:]] if n > 0 else []
        return dds.solve_board(state['trump'], first, trick, state['hands'], target, solutions, mode)


api.add_resource(DDSTable, '/api/dds-table/')



if __name__ == "__main__":
    app.run(debug=True)

    # Here is an example command to use with curl
    #curl --header "Content-Type: application/json"   --request POST   --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}'   http://localhost:5000/api/dds-table/

    # dds = DDS(max_threads=2)
    # state = {
        # 'plays': [['W', 'H8']],
        # 'hands': {
            # 'S': ['D3', 'C6', 'DT', 'D8', 'DJ', 'D6', 'CA', 'C3', 'S2', 'C2', 'C4', 'S9', 'S7'],
            # 'W': ['DA', 'S4', 'HT', 'C5', 'D4', 'D7', 'S6', 'S3', 'DK', 'CT', 'D2', 'SK'],
            # 'N': ['C7', 'H6', 'H7', 'H9', 'CJ', 'SA', 'S8', 'SQ', 'D5', 'S5', 'HK', 'C8', 'HA'],
            # 'E': ['H2', 'H5', 'CQ', 'D9', 'H4', 'ST', 'HQ', 'SJ', 'HJ', 'DQ', 'H3', 'C9', 'CK']
        # },
        # 'trump': 'N'
    # }
    # Solve for a specific position inside the play
    # print(dds_scores(dds, state, target=-1, solutions=3))

    # Generate the table at the end of the board
    # state['hands']['W'].append('H8')
    # print(dds.calc_dd_table(state['hands']))

