

$(document).ready(function () {
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
    var products = $.ajax(../);
}