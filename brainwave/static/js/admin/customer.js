var customerViewView, customerNewView;

$(function() {
    customerViewView = new CustomerViewView({el: '#customers tbody'});
    customerNewView = new CustomerNewView();
    customerAssociationView = new CustomerAssociationView();

    $('#new-btn').click(function() {
        $(this).hide();
        customerNewView.show();
    });
});

CustomerViewView = Backbone.View.extend({
    customers: new collections.Customers(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/customer/all/all', {}, function(data) {
            me.customers = new collections.Customers(data.customers);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#customer-view-template').html(),
            {customers: this.customers.models});
        this.$el.html(template);
    },
    events: {
        'click button.associations': 'associations',
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    associations: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = this.customers.get(id);

        customerAssociationView.model = customer;
        customerAssociationView.show();

        $('.associations, .edit, .remove').hide();
    },
    edit: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = this.customers.get(id);

        var customerEditView = new CustomerEditView({model: customer,
            el: $tr});

        $('.associations, .edit, .remove').hide();
    },
    remove: function(event) {
        if (!confirm('Are you sure?')) {
            return;
        }

        var me = this;
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var customer = this.customers.get(id);

        customer.destroy({
            success: function() {
                clearflash();
                flash('Customer removed successfully', 'success');

                me.update();
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
        var me = this;
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);

        set_form_values(this.model, $tr);
        this.model.save({}, {
            success: function() {
                clearflash();
                flash('Customer saved successfully', 'success');

                me.remove();
                customerViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    },
    cancel: function(event) {
        this.remove();
        customerViewView.update();
    }
});

CustomerNewView = Backbone.View.extend({
    el: '#new-customer',
    initialize: function() {
        this.hide();
    },
    show: function() {
        this.$el.show();
        this.delegateEvents();
        this.render();
    },
    hide: function() {
        this.$el.hide();
        this.undelegateEvents();
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
        var me = this;
        var $save_btn = $('button#save-new');

        $save_btn.attr('disabled', true);

        var customer = new models.Customer();
        set_form_values(customer, $('#new-customer-form'));

        customer.save({}, {
            success: function() {
                clearflash();
                flash('Customer saved successfully', 'success');

                me.hide();
                $('#new-btn').show();

                customerViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $save_btn.attr('disabled', false);
            }
        });
    },
    cancel: function(event) {
        this.hide();
        $('#new-btn').show();
    }
});

CustomerAssociationView = Backbone.View.extend({
    el: '#customer-associations',
    all_associations: new collections.Associations(),
    initialize: function() {
        this.hide();
    },
    hide: function() {
        this.$el.hide();
        this.undelegateEvents();
    },
    show: function() {
        this.$el.show();
        this.delegateEvents();
        this.update();
    },
    update: function() {
        var me = this;

        var finished = false;

        this.all_associations.fetch({
            success: function() {
                if (finished) {
                    me.update_done();
                    return;
                }

                finished = true;
            }
        });

        this.model.associations.fetch({
            success: function() {
                if (finished) {
                    me.update_done();
                    return;
                }

                finished = true;
            }
        });
    },
    update_done: function() {
        this.render();
    },
    render: function() {
        var all_associations = new collections.Associations(this.all_associations.models);
        all_associations.remove(this.model.associations.models);

        var template = _.template($('#customer-associations-template').html(),
            {customer: this.model, all_associations: all_associations.models});
        this.$el.html(template);
    },
    events: {
        'click button#add-association': 'add',
        'click button.remove-association': 'remove',
        'click button#close-associations': 'close'
    },
    add: function(event) {
        var me = this;
        var $this = $(event.currentTarget);
        $this.prop('disabled', true);
        var association_id = $('#association-id').val();

        if (!association_id) {
            clearflash();
            flash('No association selected', 'danger');
            $this.prop('disabled', false);

            return;
        }

        $.ajax('/api/customer/association/' + this.model.get('id'), {
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({association_id: association_id}),
            success: function() {
                clearflash();
                flash('Association added successfully', 'success');

                me.update();
            },
            error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    },
    remove: function(event) {
        var $this = $(event.currentTarget);
        $this.prop('disabled', true);

        if (!confirm('Are you sure?')) {
            $this.prop('disabled', false);
            return;
        }

        var me = this;
        var $tr = find_tr($this);
        var association_id = $tr.data('id');

        $.ajax('/api/customer/association/' + this.model.get('id'), {
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({association_id: association_id}),
            success: function() {
                clearflash();
                flash('Association removed successfully', 'success');

                me.update();
            },
            error: function(response) {
                ajax_error_handler(response);
                $this.prop('disabled', false);
            }
        });
    },
    close: function(event) {
        this.hide();
        $('.associations, .edit, .remove').show();
    }
});
