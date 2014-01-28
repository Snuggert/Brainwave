var transInViewView;

$(function() {
    $('select').select2();
    transInViewView = new TransInViewView({el: '#trans_in_list tbody'});

    $(document).on('click', '#new-btn', function() {
        $(this).hide();
        // var associationNewView = new TransInViewView();
    });

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
            $('div.modal#trans_in').modal('hide');
            transInViewView.update();
        }, button);
    });
});


TransInViewView = Backbone.View.extend({
    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;
        

        $.get('/api/trans_in/all', {}, function(data) {
            me.trans_in_list = new collections.Trans_in_list(data.trans_in);
            $.get('/api/stock/all', {}, function(data) {
                var stocks = new collections.Stocks(data.stocks);

                _.each(me.trans_in_list.models, function(trans_in) {
                    trans_in.stock = stocks.get(trans_in.get('stock_id'));
                });
                me.render();
            });
        });
    },
    render: function() {
        var template = _.template($('#trans-in-view-template').html(),
            {trans_in_list: this.trans_in_list.models});
        this.$el.html(template);
    },
    events: {
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    edit: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var trans_in = this.trans_in_list.get(id);

        var transInEditView = new TransInEditView({model: product_category,
            el: $tr});

        /* Hide other edit and remove buttons. */
        $('.edit, .remove').hide();
    },
    remove: function(event) {
        if (!confirm('Are you sure?')) {
            return;
        }

        var me = this;

        var $this = $(event.currentTarget);
        $this.prop('disabled', true);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var trans_in = this.trans_in_list.get(id);

        trans_in.destroy({
            success: function() {
                clearflash();
                flash('Stock transaction removed successfully', 'success');

                me.update();
            }, error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    }
});