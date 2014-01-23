'use strict';

$(function(){
    $('select').select2();
    var stock = new models.Stock(brainwave.stock);
    $('#createhide').toggle();
    $('form#new_stock').on('submit', function(e) {
        e.preventDefault();


        var button = $(this).find('button.save');
        button.button('loading');
        button.button('reset');

        set_form_values(stock, $(this));

        save_werr(stock, {}, function(model, response, options) {
            clearflash();
            button.button('reset');
            flash('De stock is aangemaakt', 'success');
            redirect('/admin/stock')
        }, button);
    });
})
