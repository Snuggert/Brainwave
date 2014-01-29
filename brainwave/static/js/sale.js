var receipt = [];
var products;
number = "";
squares = ['.product', '.number-key'];


$(document).ready(function () {
    load_products();
    add_number_keys();
    reshape_squares();
});

$(window).resize(function () {
    reshape_squares();
});

function reshape_squares () {
    for (i = 0; i < squares.length; i++) {
        var cw = $(squares[i]).width();
        $(squares[i]).css({'height': cw + 'px'});
    }
}


function load_products () {
    var result = $.ajax({
        type: "GET",
        url: "../api/product/all",
        async: false,
        success: function (data) {
            products = data.products;
            console.log(data);
            $('#product-list').html("");
            for (i = 0; i < data.products.length; i++) {
                $('#product-list').append(
                    "<a href='#' class='product btn btn-default btn-primary' " +
                    "onclick='add_product(" + products[i].id + ")'>"+ 
                    products[i].shortname + "</a>"
                );
            }
        }
        
    });
}

function add_number_keys () {
    var i = 0;
    do {
        i = (i+1) % 10;
        $('#number-pad').append(
            "<a href='#' class='number-key btn btn-default btn-primary col-md-4' " +
                "onclick='add_digit(\"" + i + "\")'>"+ 
                i+ "</a>"
        );
    } while (i != 0);
}

function load_stock () {
    var result = $.ajax({
        type: "GET",
        url: "../api/stock/all",
        async: false,
        success: function (data) {
            console.log(data);
        } 
    });
}

function add_product (id) {
    if (!number) {
        number = "1";
    }
    if (receipt[id]) {
        receipt[id] += parseInt(number);
    }
    else {
        receipt[id] = parseInt(number);
    }
    number = "";
    console.log("receipt", receipt);
    display_receipt();
}

function add_digit (digit) {
    number = number.concat(digit);
    console.log("number:", number);
}

function display_receipt () {
    var total = 0;
    $("#receipt-items").html("");
    for (var i = 0; i < receipt.length; i++) {
        if (receipt[i]) {
            console.log("display", i, product_by_id(i));
            var product = products[product_by_id(i)];
            console.log(product);
            $("#receipt-items").append(
                "<div>" + product.shortname + " " + receipt[i].toString() + 
                " &euro;" + product.price*receipt[i] + 
                "<a class='btn' onclick='receipt_remove("+i+")'>X</a></div>"
            );
            total += product.price*receipt[i];
        }
        
    }
    $("#receipt-items").append("<div>total: &euro;" + total + "</div>");
}


function complete_transaction (pay_type) {
    var items ="[";
    for (var i = 0; i < receipt.length; i++) {
        if (receipt[i]) {
            for (var j = 0; j < receipt[i]; j++) {
                    items = items.concat('{"product_id":' + i.toString() + ', "action":"sell"},');
            }
        }
    }
    // remove the last , .
    items = items.substr(0, items.length-1);
    items = items.concat("]");
    
    $(document).ready(function(){
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "../api/transaction/new",
            async: false,
            data: '{"pay_type": "'+ pay_type +'", "items": '+ items +'}',
            dataType: "json"
        });
    });
    receipt = [];
    display_receipt();
}

function receipt_remove (index) {
    receipt[index] = 0;
    display_receipt();
}

function product_by_id(id) {
    for (var i = 0; i < products.length; i++) {
        console.log("by_id", i, products[i].id, id);
        if (products[i].id == id) {
            return i;
        }
    }
    return false;
}