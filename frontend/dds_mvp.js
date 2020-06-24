// Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
//
//   Use of this source code is governed by an MIT-style
//   license that can be found in the LICENSE file or at
//   https://opensource.org/licenses/MIT

"use strict";

const DIRECTIONS = ["north", "east", "south", "west"];
const SUITS = ["spades", "hearts", "diamonds", "clubs"];
const PIPS = "AKQJT98765432";


function fillFormWithTestData(nesw) {
    var holdings = [];

    for (const hand of nesw) {
        for (const holding of hand.split(".")) {
            holdings.push(holding);
        }
    }

    for (const element of hand_elements()) {
        element.value = holdings.shift();
    }
}

function fillFormWithGrandSlamTestData() {
    fillFormWithTestData([
        "AKQJ.AKQJ.T98.T9",
        "5432.5432.32.432",
        "T98.T9.AKQJ.AKQJ",
        "76.876.7654.8765"
    ]);
}

function fillFormWithEveryoneMakes3nTestData() {
    fillFormWithTestData([
        "QT9.A8765432.KJ.",
        "KJ..A8765432.QT9",
        "A8765432.QT9..KJ",
        ".KJ.QT9.A8765432"
    ]);
}

function fillFormWithPartScoreTestData() {
    fillFormWithTestData([
        "AQ85.AK976.5.J87",
        "JT.QJ5432.Q9.KQ9",
        "972..JT863.A6432",
        "K643.T8.AK742.T5"
    ]);
}

function * directions_and_suits() {
    // Generator

    for (var direction_index = 0; direction_index < 4; direction_index++ ) {
        const direction = DIRECTIONS[direction_index];

        for (var suit_index = 0; suit_index < 4; suit_index++) {
            const suit = SUITS[suit_index];

            yield { "direction": direction, "suit": suit };
        }
    }
}

function * hand_elements() {
    // Generator

    for (const ds of directions_and_suits()) {
        var element_index = ds["direction"] + "_" + ds["suit"];
        var element = document.getElementById(element_index);
        yield element;
    }
}

function clearTestData() {
    for (const element of hand_elements()) {
        element.value = "";
    }
}

function rotateClockwise() {
    var hands = [];

    for (const element of hand_elements()) {
        hands.push(element.value);
    }

    // rotate west to north, and so on
    for (var i = 0; i < 4; i++) {
        var west = hands.pop();
        hands.unshift(west);
    }

    for (const element of hand_elements()) {
        element.value = hands.shift();
    }
}

function collectHands() {
    var hands = {};

    for (const ds of directions_and_suits()) {
        var direction_letter = ds["direction"].charAt(0).toUpperCase();
            hands[direction_letter] = hands[direction_letter] || [];

        var suit_letter = ds["suit"].charAt(0).toUpperCase();
        var element_index = ds["direction"] + "_" + ds["suit"];
        var holding = document.getElementById(element_index).value;

        for (const card of holding) {
            hands[direction_letter].push(suit_letter + card.toUpperCase());
        }
    }

    return hands;
}

function inputIsValid(hands) {
    // TODO Make sure no card is repeated.

    for (const direction in hands) {
        const hand = hands[direction];

        if (hand.length != 13) {
            return "Please enter 13 cards per hand.";
        }
        
        for (const card of hand) {
            const pip = card.substring(1);
            if (!PIPS.includes(pip)) {
                return "Please use only these pips: " + PIPS;
            }
        }
    }

    return "";
}

function pageLoad() {    
    document.getElementById("valid-pips").innerHTML = PIPS;
}

function sendJSON() {
    var hands = collectHands();

    const error_message = inputIsValid(hands);

    if (error_message.length == 0) {
        var xhr = new XMLHttpRequest();
        const URL = "http://localhost:5000/api/dds-table/";

        // This fails as of 2020-06-21 due to:
        // Access from origin 'null' has been blocked by CORS policy
        // That's because an older version of our service is deployed.
        // const URL = "https://dds.hackathon.globalbridge.app/api/dds-table/";

        xhr.open("POST", URL, true);

        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                document.getElementById("result").innerHTML = this.responseText;
            }
        };

        document.getElementById("result").innerHTML = "";
        var deal = { "hands": hands };
        var data = JSON.stringify(deal);
        xhr.send(data);
    } else {
        document.getElementById("result").innerHTML = error_message;
    }
}
