var customerViewView;

$(function() {
    customerViewView = new CustomerViewView();

    $('#new-btn').click(function() {
        $(this).hide();
        var customerNewView = new CustomerNewView();
    });
});

CustomerViewView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        $.get('/api/customer/all', {}, function(data) {
            customers = new collections.Customers(data.customers);
            customerViewView.render();

            var template = _.template($('#customer-view-template').html(),
                {customers: customers.models});
            $('#customers tbody').html(template);
        });
    },
    events: {
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    edit: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = customers.get(id);

        var customerEditView = new CustomerEditView({model: customer,
            el: $tr});

        /* Hide other edit and remove buttons. */
        $('.edit, .remove').hide();
    },
    remove: function(event) {
        if (!confirm('Are you sure?')) {
            return;
        }

        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = customers.get(id);

        customer.destroy({
            success: function() {
                clearflash();
                flash('Customer removed successfully', 'success');

                reload_list();
            }, error: function(response) {
                ajax_error_handler(response);
            }
        });
    }
});

CustomerEditView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#customer-edit-template').html(),
            {customer: this.model});
        this.$el.html(template);
    },
    events: {
        'click button.save': 'save',
        'click button.cancel': 'cancel'
    },
    save: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = customers.get(id);

        set_form_values(customer, $tr);
        customer.save({}, {
            success: function() {
                clearflash();
                flash('Customer saved successfully', 'success');

                reload_list();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    },
    cancel: function(event) {
        reload_list();
    }
});

CustomerNewView = Backbone.View.extend({
    el: '#new-customer',
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#customer-new-template').html());
        this.$el.html(template);
    },
    events: {
        'click button#save-new': 'save',
        'click button#cancel-new': 'cancel'
    },
    save: function(event) {
        var $save_btn = $('button#save-new');

        $save_btn.attr('disabled', true);

        var customer = new models.Customer();
        set_form_values(customer, $('#new-customer-form'));

        var view = this;
        customer.save({}, {
            success: function() {
                clearflash();
                flash('Customer saved successfully', 'success');

                view.cancel();
                reload_list();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $save_btn.attr('disabled', false);
            }
        });
    },
    cancel: function(event) {
        this.$el.empty();
        $('#new-btn').show();
    }
});
