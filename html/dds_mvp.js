// Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
//
//   Use of this source code is governed by an MIT-style
//   license that can be found in the LICENSE file or at
//   https://opensource.org/licenses/MIT

function sendJSON(){        
    xhr = new XMLHttpRequest(); 
    url = "http://localhost:5000/api/dds-table/"; 

    xhr.open("POST", url, true); 

    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 
            document.getElementById("result").innerHTML = this.responseText;
            document.getElementById("log").innerHTML = "nothing to log yet";
        }
    }; 

    // deal = {"hands":{"N": ["SA"], "E": ["HA"], "S": ["DA"], "W": ["CA"]}}

    // Build the structure from the form fields
    var directions = ['north', 'east', 'south', 'west'];
    var suits = ['clubs', 'diamonds', 'hearts', 'spades']

    var deal = {};
    
    for (direction of directions) {
        deal[direction] = {}
        
        for (suit of suits) {
            deal[direction][suit] = document.getElementById("north spades").value
        }
    }

    console.log(deal)

    deal = {"hands": {
                 "S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],
                 "W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK", "H8"],
                 "N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],
                 "E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]
                }}
                
    var data = JSON.stringify(deal); 
    xhr.send(data); 
} 
