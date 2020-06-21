// Copyright 2020 Adam Wildavsky and the Bridge Hackathon contributors
//
//   Use of this source code is governed by an MIT-style
//   license that can be found in the LICENSE file or at
//   https://opensource.org/licenses/MIT

"use strict";

const DIRECTIONS = ["north", "east", "south", "west"];
const SUITS = ["spades", "hearts", "diamonds", "clubs"];


function fillFormWithTestData(nesw) {
    for (var direction_index = 0; direction_index < 4; direction_index++ ) {
        var hand = nesw[direction_index];
        var direction = DIRECTIONS[direction_index];

        var holdings = hand.split(".");

        for (var suit_index = 0; suit_index < 4; suit_index++) {
            var suit = SUITS[suit_index];
            var holding = holdings[suit_index];
            var element_index = direction + "_" + suit;
            var element = document.getElementById(element_index);
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

function clearTestData() {
    for (var direction_index = 0; direction_index < 4; direction_index++ ) {
        var direction = DIRECTIONS[direction_index];

        for (var suit_index = 0; suit_index < 4; suit_index++) {
            var suit = SUITS[suit_index];
            var element_index = direction + "_" + suit;
            var element = document.getElementById(element_index);
            element.value = "";
        }
    }
}

function rotateClockwise() {
    var old_hands = [];

    for (var direction_index = 0; direction_index < 4; direction_index++ ) {
        var old_direction = DIRECTIONS[direction_index];
        var new_direction = DIRECTIONS[(direction_index + 1) % 4];

        old_hands.push([]);

        for (var suit_index = 0; suit_index < 4; suit_index++) {
            var suit = SUITS[suit_index];
            var element_index = old_direction + "_" + suit;
            var old_element = document.getElementById(element_index);
            var old_value = old_element.value;
            old_hands[direction_index].push(old_value);
        }
    }

    for (var direction_index = 0; direction_index < 4; direction_index++ ) {
        var new_direction = DIRECTIONS[(direction_index + 1) % 4];

        for (var suit_index = 0; suit_index < 4; suit_index++) {
            var suit = SUITS[suit_index];
            var element_index = new_direction + "_" + suit;
            var new_element = document.getElementById(element_index);
            new_element.value = old_hands[direction_index][suit_index];
        }
    }
}

function collectHands() {
    var hands = {};

    for (var direction of DIRECTIONS) {
        var direction_letter = direction.charAt(0).toUpperCase();
        hands[direction_letter] = [];

        for (var suit of SUITS) {
            var suit_letter = suit.charAt(0).toUpperCase();
            var element_index = direction + "_" + suit;
            var holding = document.getElementById(element_index).value;

            for (var card of holding) {
                hands[direction_letter].push(suit_letter + card.toUpperCase());
            }
       }
    }

    return hands;
}

function sendJSON(){
    var xhr = new XMLHttpRequest();
    const URL = "http://localhost:5000/api/dds-table/";

    xhr.open("POST", URL, true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("result").innerHTML = this.responseText;
        }
    };

    var hands = collectHands();
    var deal = { "hands": hands };
    var data = JSON.stringify(deal);
    xhr.send(data);
}
