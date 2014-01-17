'use strict';

$(function(){
    $('select').select2();
    var product = new models.Product(brainwave.product);
    $('form#new_product').on('submit', function(e) {
        e.preventDefault();
        var button = $(this).find('button.save');
        button.button('loading');
        button.button('reset');
        set_form_values(product, $(this));

        save_werr(product, {}, function(model, response, options) {
            clearflash();
            button.button('reset');
            flash('Het product is aangemaakt', 'success');
            redirect('/admin/product')
        }, button);
    });
})