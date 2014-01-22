var associationViewView;

$(function() {
    associationViewView = new AssociationViewView({el: '#associations tbody'});

    $('#new-btn').click(function() {
        $(this).parents('.panel-body').hide();
        var associationNewView = new AssociationNewView();
    });
});

/* Backbone stuff. */
AssociationViewView = Backbone.View.extend({
    associations: new collections.Associations(),
    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/association/all', {}, function(data) {
            me.associations = new collections.Associations(data.associations);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#association-view-template').html(),
            {associations: this.associations.models});
        this.$el.html(template);
    },
    events: {
        'click button.members': 'members',
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    members: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var association = this.associations.get(id);

        var associationCustomerView =
            new AssociationCustomerView({model: association,
                                         el: '#association-members'});

        $('.members, .edit, .remove').hide();
    },
    edit: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var association = this.associations.get(id);

        var associationEditView = new AssociationEditView({model: association,
            el: $tr});

        /* Hide other edit and remove buttons. */
        $('.members, .edit, .remove').hide();
    },
    remove: function(event) {
        if (!confirm('Are you sure?')) {
            return;
        }

        var me = this;

        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var association = this.associations.get(id);

        association.destroy({
            success: function() {
                clearflash();
                flash('Association removed successfully', 'success');

                me.update();
            }, error: function(response) {
                ajax_error_handler(response);
            }
        });
    }
});

AssociationEditView = Backbone.View.extend({
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#association-edit-template').html(),
            {association: this.model});
        this.$el.html(template);
    },
    events: {
        'click button.cancel': 'cancel',
        'click button.save': 'save'
    },
    cancel: function(event) {
        associationViewView.update();
    },
    save: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var association = associationViewView.associations.get(id);

        set_form_values(association, $tr);
        association.save({}, {
            success: function() {
                clearflash();
                flash('Association saved successfully', 'success');

                associationViewView.render();
            }, error: function(model, response) {
                ajax_error_handler(response);
            }
        });
    }
});

AssociationNewView = Backbone.View.extend({
    el: '#new-association',

    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#association-new-template').html());
        this.$el.html(template);
    },
    events: {
        'click button#cancel-new': 'cancel',
        'click button#save-new': 'save'
    },
    cancel: function(event) {
        this.$el.empty();
        $('#new-btn').parents('.panel-body').show();
    },
    save: function(event) {
        $('button#save-new').attr('disabled', true);

        var association = new models.Association();
        set_form_values(association, $('#new-association-form'));

        var view = this;
        association.save({}, {
            success: function() {
                clearflash();
                flash('Association successfully saved', 'success');

                view.cancel();
                associationViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});

AssociationCustomerView = Backbone.View.extend({
    customers: new collections.Customers(),
    all_customers: new collections.Customers(),
    initialize: function() {
        var me = this;

        $.get('/api/customer/all',
            function(data) {
                me.all_customers = new collections.Customers(data.customers);
                me.update();
            });
    },
    update: function() {
        var me = this;

        $.get('/api/association/customer/' + this.model.get('id'),
            function(data) {
                me.customers = new collections.Customers(data.customers);
                me.render();
            });
    },
    render: function() {
        var all_customers = new collections.Customers(this.all_customers.models);
        all_customers.remove(this.customers.models);

        var template = _.template($('#association-customers-template').html(),
            {association: this.model, customers: this.customers.models,
             all_customers: all_customers.models});
        this.$el.html(template);
    },
    events: {
        'click button#add-customer': 'add',
        'click button.remove-customer': 'remove',
        'click button#close-customer': 'close'
    },
    add: function(event) {
        var me = this;
        var customer_id = $('#customer-id').val();

        $.ajax('/api/association/customer/' + this.model.get('id'), {
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({customer_id: customer_id}),
            success: function() {
                clearflash();
                flash('Customer added successfully', 'success');

                me.update();
            },
            error: function(response) {
                ajax_error_handler(response);
            }
        });
    },
    remove: function(event) {
        if (!confirm('Are you sure?')) {
            return;
        }

        var me = this;
        var $tr = find_tr($(event.currentTarget));
        var customer_id = $tr.data('id');

        $.ajax('/api/association/customer/' + this.model.get('id'), {
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({customer_id: customer_id}),
            success: function() {
                clearflash();
                flash('Customer removed successfully', 'success');

                me.update();
            },
            error: function(response) {
                ajax_error_handler(response);
            }
        });
    },
    close: function(event) {
        $('.members, .edit, .remove').show();
        this.$el.empty();
    }
});
