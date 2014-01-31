var productViewView;

$(function() {
    productViewView = new ProductViewView({el: '#products tbody'});

    $('#new-btn').click(function() {
        $(this).parents('.panel-body').hide();
        var productNewView = new ProductNewView({el: '#new-product'});
        $(this).hide();
    });
});

/* Backbone stuff. */
var ProductViewView = Backbone.View.extend({
    products: new collections.Products(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/product/all', {}, function(data) {
            me.products = new collections.Products(data.products);

            $.get('/api/stock/all', {}, function(data) {
                var stocks = new collections.Stocks(data.stocks);
                _.each(me.products.models, function(product) {
                    product.stock = stocks.get(product.get('stock_id'));
                });
                $.get('/api/product_category/all', {}, function(data) {
                    var product_categories = new collections.ProductCategories(data.product_categories);
                    _.each(me.products.models, function(product) {
                        product.product_category = product_categories.get(product.get('product_category_id'));
                    });
                    me.render();
                });
            });
        });
    },
    render: function() {
        var template = _.template($('#product-view-template').html(), {
            products: this.products.models
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
        var product = this.products.get(id);

        var productEditView = new ProductEditView({model: product, el: $tr});

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
        var product = this.products.get(id);

        product.destroy({
            success: function() {
                clearflash();
                flash('Product removed successfully', 'success');

                me.update();
            }, error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    }
});

var ProductEditView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#product-edit-template').html(),
            {product: this.model});
        this.$el.html(template);
    },
    events: {
        'click button.cancel': 'cancel',
        'click button.save': 'save'
    },
    cancel: function(event) {
        productViewView.update();
    },
    save: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var product = productViewView.products.get(id);

        set_form_values(product, $tr);
        product.save({}, {
            success: function() {
                clearflash();
                flash('Product saved successfully', 'success');

                productViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    }
});

var ProductNewView = Backbone.View.extend({
    stocks: new collections.Stocks(),
    product_categories: new collections.ProductCategories(),
    associations: new collections.Associations(),
    initialize: function() {
        var me = this;
        $.get('/api/stock/all', {}, function(data) {
            me.stocks = new collections.Stocks(data.stocks);
            $.get('/api/association/all', {}, function(data) {
                me.associations = new collections.Associations(data.associations);
                $.get('/api/product_category/all', {}, function(data) {
                    me.product_categories = new collections.ProductCategories(data.product_categories);
                    me.render();
                });
            });
        });
    },
    render: function() {
        var template = _.template($('#product-new-template').html(), {
            stocks: this.stocks.models,
            product_categories: this.product_categories.models,
            associations: this.associations.models
        });
        this.$el.html(template);
        $('select').select2();
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

        var product = new models.Product();
        set_form_values(product, $('#new-product-form'));

        var view = this;
        product.save({}, {
            success: function() {
                clearflash();
                flash('Product successfully saved', 'success');
                view.cancel();
                $('#new-btn').show();
                productViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});
