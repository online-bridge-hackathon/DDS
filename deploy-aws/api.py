from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from dds import DDS

import yaml

# Configuration filename
# config_filename = "server.yaml"

# Default for maximum threads is to let the library decide
mt = 0
# Default for maximum memory is to let the library decide
mm = 0

app = Flask(__name__)

config = {}
#try:
#    with open(config_filename) as config_handle:
#        config = yaml.safe_load(config_handle)
#        libdds_config = config.get('libdds', {})
#        mm = libdds_config.get('max_memory', mm)
#        mt = libdds_config.get('max_threads', mt)
#except (yaml.YAMLError, AttributeError) as err:
#    app.logger.critical(f"Unable to parse configuration {config_filename}: "
#                        f"{err}")
#    raise
#except Exception as err:
#    app.logger.warning(f"Unable to load configuration {config_filename}: "
#                       f"{err}")
#    app.logger.warning("Using the default configuration.")

app.config.from_mapping(config.get('flask', {}))
CORS(app)
api = Api(app)

# When SetMaxThreads is called there must not be any other threads calling
# libdds. The easiest way to avoid parallel calls is to keep only one DDS
# object as long as server runs.
dds = DDS(max_threads=mt, max_memory=mm)


class DDSTable(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        """Takes in a single hand and returns a DDS table"""
        data = request.get_json()
        # Verify the data here
        # self.verifyinput(data)
        dds_table = dds.calc_dd_table(data['hands'])
        return dds_table


class DDSScore(Resource):
    def post(self):
        """This should hook in to the dds_scores function listed below"""
        raise NotImplementedError()

    def dds_scores(self, dds, state, target, solutions, mode=1):
        """Gives the dds score for the given contract, may be mid-hand"""
        n = len(state['plays']) % 4
        first = state['plays'][-n][0] if n > 0 else state['turn']
        trick = [c for _, c in state['plays'][-n:]] if n > 0 else []
        return dds.solve_board(state['trump'], first, trick, state['hands'],
                               target, solutions, mode)


api.add_resource(DDSTable, '/api/dds-table/')

if __name__ == "__main__":
    app.run(debug=True)

    # Here is an example command to use with curl
    # curl --header "Content-Type: application/json"   --request POST   --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}'   http://localhost:5000/api/dds-table/

    # Example input format
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

