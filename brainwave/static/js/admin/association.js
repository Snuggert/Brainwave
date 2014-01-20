/* Backbone stuff. */
associations = new collections.Associations(brainwave.associations);

AssociationViewView = Backbone.View.extend({
    el: '#associations tbody',

    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($('#association-view-template').html(),
            {associations: associations.models});
        this.$el.html(template);
    },
    events: {
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    edit: function(event) {
        edit_click($(event.currentTarget));
    },
    remove: function(event) {
        remove_click($(event.currentTarget));
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
        reset_list();
    },
    save: function(event) {
        save_click($(event.currentTarget));
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
        $('#new-btn').show();
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
                reset_list();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});

var associationViewView;

$(function() {
    associationViewView = new AssociationViewView();
});

/* What happens when the edit button is clicked. */
function edit_click($el) {
    var $tr = find_tr($el);
    var id = $tr.data('id');
    var association = associations.get(id);
    var associationEditView = new AssociationEditView({model: association,
        el: $tr});

    /* Hide other edit and remove buttons. */
    $('.edit, .remove').hide();
}

function reset_list() {
    $.get('/api/association/all', {}, function(data) {
        brainwave.associations = data.associations;
        associations = new collections.Associations(brainwave.associations);
        associationViewView.render();
    });
}

/* What happens when the save button is clicked. */
function save_click($el) {
    var $tr = find_tr($el);
    var id = $tr.data('id');
    var association = associations.get(id);

    set_form_values(association, $tr);
    association.save({}, {
        success: function() {
            clearflash();
            flash('Association saved successfully', 'success');

            reset_list();
        }, error: function(response) {
            ajax_error_handler(response);
        }
    });
}

/* What happens when the remove button is clicked. */
function remove_click($el) {
    if (!confirm('Are you sure?')) {
        return;
    }

    var $tr = find_tr($el);
    var id = $tr.data('id');
    var association = associations.get(id);

    association.destroy({
        success: function() {
            clearflash();
            flash('Association removed successfully', 'success');

            reset_list();
        }, error: function(response) {
            ajax_error_handler(response);
        }
    });
}

$(function() {
    $('#new-btn').click(function() {
        $(this).hide();
        var associationNewView = new AssociationNewView();
    });
});
