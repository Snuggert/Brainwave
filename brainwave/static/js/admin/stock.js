'use strict';

var stockViewView;
$(function() {
    $('#new-btn').click(function() {
        $(this).parents('.panel-body').hide();
        $('#stockmodal').modal('show')
        var stockNewView = new StockNewView({el: '#new-stock'});
        $(this).hide();
    });
    stockViewView = new StockViewView({el: '#all_stocks tbody'});
});

/* Backbone stuff. */
var StockViewView = Backbone.View.extend({
    stocks: new collections.Stocks(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/stock/all', {}, function(data) {
            me.stocks = new collections.Stocks(data.stocks);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#stock-view-template').html(), {
            stocks: this.stocks.models
        });
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
        var stock = this.stocks.get(id);

        var stockEditView = new StockEditView({model: stock,
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
        var stock = this.stocks.get(id);

        stock.destroy({
            success: function() {
                clearflash();
                flash('Stock removed successfully', 'success');

                me.update();
            }, error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    }
});

var StockEditView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#stock-edit-template').html(),
            {stock: this.model});
        this.$el.html(template);
    },
    events: {
        'click button.cancel': 'cancel',
        'click button.save': 'save'
    },
    cancel: function(event) {
        stockViewView.update();
    },
    save: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var stock = stockViewView.stocks.get(id);

        set_form_values(stock, $tr);
        stock.save({}, {
            success: function() {
                clearflash();
                flash('Stock saved successfully', 'success');

                stockViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    }
});

var StockNewView = Backbone.View.extend({

    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#stock-new-template').html());
        this.$el.html(template);
        $('[data-toggle="tooltip"]').tooltip({
            'placement': 'top'
        });
    },
    events: {
        'click button#cancel-new': 'cancel',
        'click button#save-new': 'save'
    },
    cancel: function(event) {
        this.$el.empty();
        $('#new-btn').parents('.panel-body').show();
        $('#new-btn').show()
    },
    save: function(event) {
        $('button#save-new').attr('disabled', true);

        var stock = new models.Stock();
        set_form_values(stock, $('#new-stock-form'));

        var view = this;
        stock.save({}, {
            success: function() {
                clearflash();
                flash('Stock successfully saved', 'success');
                view.cancel();
                $('#new-btn').show();
                stockViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});
