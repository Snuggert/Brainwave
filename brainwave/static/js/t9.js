/*
var names = ["Bas Klaplong", "Bram van den Akker", "Jaap Koetsier", "Mats ten Bohmer",
             "Stein van Zwoll", "Sander", "Juliën", "Pieter", "Gijs", "ÛØËÎ"];
names.sort();
*/
var customers;
var letters = ["clear", "space", "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"];
var letters_acc = ["clear", " ", "ABCÀÁÅÃÆÇàáâãäåæç", "DEFÈÉÊËèéêë", "GHIÌÍÎÏìíîï", 
                   "JKL", "MNOÑñÒÓÔÕÖØòóôõöøð", "PQRSß", "TUVÙÚÛÜùúûü", "WXYZýþÿÝÞ"];
var squares = ['.number-key'];
var pattern = "";
var numbers = "";

$(document).ready(function () {
    load_customers();
    add_number_keys();
    reshape_squares();
    display_names();
});

function add_to_pattern (number) {
    if (letters[number]) {
        pattern = pattern + "[" + letters_acc[number] + "]";
        numbers = numbers + number;
    }
    if (letters[number] == "clear") {
        pattern = "";
        numbers = "";
    }
    //console.log(pattern);
    display_names();
}

function pattern_backspace () {
    numbers = numbers.substr(0, numbers.length-1);
    pattern = pattern.substr(0, pattern.lastIndexOf("["));
    display_names();
}

function display_names () {
    $("#names").html("");
    $("#names").append(numbers + "<br />");
    var filter = new RegExp(pattern, "i");
    for (var i = 0; i < customers.length; i++) {
        name = customers[i].name;
        matches = filter.exec(name);
        if (!filter || matches) {
            var match = matches[0];
            match_pos = name.indexOf(match);
            $("#names").append("<a onclick='select_customer(\"" + i + "\")'>" + 
                               name.substr(0,match_pos) + "<b>" +  
                               name.substr(match_pos, match.length) +
                               "</b>" + name.substr(match_pos + match.length, name.length) +
                               "</a>" + "<br />");
        }
    }
}

function reshape_squares () {
    for (i = 0; i < squares.length; i++) {
        var cw = $(squares[i]).width();
        $(squares[i]).css({'height': cw + 'px'});
    }
}

function select_customer (id) {
    alert(customers[id].name + " selected.");
    pattern = "";
    numbers = "";
    display_names();
}

function add_number_keys () {
    var i = 0;
    do {
        i = (i+1) % 10;
        $('#number-pad').append(
            "<a href='#' class='number-key btn btn-default btn-primary col-md-4' " +
                "onclick='add_to_pattern(\"" + i + "\")'>"+ 
                i+ " " + letters[i] + "</a>"
        );
    } while (i != 0);
    
    $('#number-pad').append(
        "<a href='#' class='number-key btn btn-default btn-primary col-md-4' " +
            "onclick='pattern_backspace()'>backspace</a>"
    );
}

function load_customers () {
    var result = $.ajax({
        type: "GET",
        url: "/api/customer/all",
        async: false,
        success: function (data) {
            console.log(data);
            customers=data.customers;
        }  
    });
}