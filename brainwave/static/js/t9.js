var names = ["Bas Klaplong", "Bram van den Akker", "Jaap Koetsier", "Mats ten Bohme",
             "Stein van Zwoll", "Sander", "Juliën", "Pieter", "Gijs", "ÛØËÎ"];
var letters = ["clear", "space", "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"];
var letters_acc = ["clear", " ", "ABCÀÁÅÃÆÇàáâãäåæç", "DEFÈÉÊËèéêë", "GHIÌÍÎÏìíîï", 
                   "JKL", "MNOÑñÒÓÔÕÖØòóôõöøð", "PQRSß", "TUVÙÚÛÜùúûü", "WXYZýþÿÝÞ"];
var squares = ['.number-key'];
var pattern = "";


$(document).ready(function () {
    add_number_keys();
    reshape_squares();
    display_names();
});

function add_to_pattern (number) {
    if (letters[number]) {
        pattern = pattern + "[" + letters_acc[number] + "]";  
    }
    if (letters[number] == "clear") {
        pattern = "";
    }
    console.log(pattern);
    display_names();
}

function display_names () {
    $("#names").html("");
    var filter = new RegExp(pattern, "i");
    for (var i = 0; i < names.length; i++) {
        if (!filter || filter.test(names[i])) {
            $("#names").append(names[i] + "<br />");
        }
    }
}

function reshape_squares () {
    for (i = 0; i < squares.length; i++) {
        var cw = $(squares[i]).width();
        $(squares[i]).css({'height': cw + 'px'});
    }
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
}