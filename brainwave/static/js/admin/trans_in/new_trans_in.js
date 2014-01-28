$(document).ready(function () {
    $('select').select2();
    $('#createhide').toggle();
    
    $('form#new_trans_in').on('submit', function(e) {
        e.preventDefault();

        var button = $(this).find('button.save');
        button.button('loading');
        button.button('reset');
        var trans_in = new models.Trans_in(brainwave.trans_in);
        set_form_values(trans_in, $(this));

        save_werr(trans_in, {}, function(model, response, options) {
            clearflash();
            button.button('reset');
            flash('De trans_in is aangemaakt', 'success');
            redirect('/admin/trans_in');
        }, button);
    });
});