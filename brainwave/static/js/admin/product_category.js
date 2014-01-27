var productCategoryViewView;

$(function() {
    productCategoryViewView = new ProductCategoryViewView({el: '#product_categories tbody'});

    $('#new-btn').click(function() {
        $(this).parents('.panel-body').hide();
        var productCategoryNewView = new ProductCategoryNewView();
        $(this).hide();
    });
});

/* Backbone stuff. */
ProductCategoryViewView = Backbone.View.extend({
    product_categories: new collections.ProductCategories(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/product_category/all', {}, function(data) {
            me.product_categories = new collections.ProductCategories(data.product_categories);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#product_category-view-template').html(), {
            product_categories: this.product_categories.models
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
        var product_category = this.product_categories.get(id);

        var productCategoryEditView = new ProductCategoryEditView({model: product_category,
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
        var product_category = this.product_categories.get(id);

        product_category.destroy({
            success: function() {
                clearflash();
                flash('Product category removed successfully', 'success');

                me.update();
            }, error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    }
});

ProductCategoryEditView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#product_category-edit-template').html(),
            {product_category: this.model});
        this.$el.html(template);
        $('input.color').colorpicker();
    },
    events: {
        'click button.cancel': 'cancel',
        'click button.save': 'save'
    },
    cancel: function(event) {
        productCategoryViewView.update();
    },
    save: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var product_category = productCategoryViewView.product_categories.get(id);

        set_form_values(product_category, $tr);
        product_category.save({}, {
            success: function() {
                clearflash();
                flash('Product category saved successfully', 'success');

                productCategoryViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    }
});

ProductCategoryNewView = Backbone.View.extend({
    el: '#new-product_category',

    initialize: function() {
        this.render();
        $('#new-product_category-color').colorpicker();
    },
    render: function() {
        var template = _.template($('#product_category-new-template').html());
        this.$el.html(template);
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

        var product_category = new models.ProductCategory();
        set_form_values(product_category, $('#new-product_category-form'));

        var view = this;
        product_category.save({}, {
            success: function() {
                clearflash();
                flash('Product category successfully saved', 'success');
                view.cancel();
                $('#new-btn').show();
                productCategoryViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});
