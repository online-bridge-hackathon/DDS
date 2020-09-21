#   Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors.
#   Use of this source code is governed by an MIT-style
#   license that can be found in the LICENSE file or at
#   https://opensource.org/licenses/MIT

from src.dds import DDS


def dds(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows POST requests from any origin with the Content-Type
        # header and caches the preflight response for 3600 seconds.
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Allow connections from any domain (CORS)
    headers = {
        'Access-Control-Allow-Origin': '*',
    }

    data = request.get_json(silent=True)
    dds_table = DDS().calc_dd_table(data['hands'])
    return (dds_table, 200, headers)
