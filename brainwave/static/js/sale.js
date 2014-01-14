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
                    "<a href='#' class='product btn'>"+ 
                    data.products[i].shortname + "</a>"
                );
            }
        }
    });

}