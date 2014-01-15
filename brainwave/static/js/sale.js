var receipt = [];

$(document).ready(function () {
    load_products();
    reshape_product();
    var products = new Backbone.Collection();
});

$(window).resize(function () {
    reshape_product();
});

function reshape_product () {
    var cw = $('.product').width();
    $('.product').css({'height': cw + 'px'});
}

function load_products () {
    var result = $.ajax({
        type: "GET",
        url: "../api/product/all",
        async: false,
        success: function (data) {
            console.log(data);
            for (i = 0; i < data.products.length; i++) {
                $('#product-list').append(
                    "<a href='#' class='product btn btn-default btn-primary' " +
                    "onclick='add_product(" + data.products[i].id + ")'>"+ 
                    data.products[i].shortname + "</a>"
                );
            }
        }
    });
}

function add_product (id) {
    receipt.push({"product_id": id.toString(), "action":"sell"});
}

function complete_transaction (pay_type) {
    $(document).ready(function(){
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "../api/transaction/new",
            data: '{"pay_type": "'+ pay_type +'", "items": '+ JSON.stringify(receipt) +'}',
            dataType: "json"
        });
    });
    receipt = [];
}