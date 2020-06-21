// Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
//
//   Use of this source code is governed by an MIT-style
//   license that can be found in the LICENSE file or at
//   https://opensource.org/licenses/MIT

const DIRECTIONS = ['north', 'east', 'south', 'west'];
const SUITS = ['spades', 'hearts', 'diamonds', 'clubs']


function fillFormWithTestData(nesw) {
    for (direction_index = 0; direction_index < 4; direction_index++ ) {
        hand = nesw[direction_index];
        direction = DIRECTIONS[direction_index];
        
        holdings = hand.split('.')
        
        for (suit_index = 0; suit_index < 4; suit_index++) {
            suit = SUITS[suit_index];
            holding = holdings[suit_index];
            index = direction + " " + suit
            console.log(index)
            console.log(holding)
            element = document.getElementById(index)
            element.value = holding;
        }
    }
}

function fillFormWithGrandSlamTestData() {
    fillFormWithTestData([
        "AKQJ.AKQJ.T98.T9",
        "5432.5432.32.432",
        "T98.T9.AKQJ.AKQJ",
        "76.876.7654.8765"
    ])
}

function clearTestData() {
    for (direction_index = 0; direction_index < 4; direction_index++ ) {
        direction = DIRECTIONS[direction_index];
                
        for (suit_index = 0; suit_index < 4; suit_index++) {
            suit = SUITS[suit_index];
            index = direction + " " + suit
            element = document.getElementById(index)
            element.value = "";
        }
    }
}

function collectHands() {
    // Build the structure from the form fields
    var hands = {};
    
    for (direction of DIRECTIONS) {
        direction_letter = direction.charAt(0).toUpperCase()        
        hands[direction_letter] = []

        for (suit of SUITS) {
            suit_letter = suit.charAt(0).toUpperCase()
            index = direction + " " + suit
            holding = document.getElementById(index).value

            for (card of holding) {
                hands[direction_letter].push(suit_letter + card.toUpperCase())
            }
       }
    }
    
    return hands;
}

function sendJSON(){        
    xhr = new XMLHttpRequest(); 
    url = "http://localhost:5000/api/dds-table/"; 

    xhr.open("POST", url, true); 

    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 
            document.getElementById("result").innerHTML = this.responseText;
        }
    }; 

    hands = collectHands();
    deal = { "hands": hands }
    var data = JSON.stringify(deal); 
    console.log(data)
    xhr.send(data); 
}
