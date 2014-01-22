$( document ).ready(function() {

    // $(document).on('click', '.delete_trans_in', function(){
    //     var request = $.ajax({
    //         url: "/api/trans_in/delete/" + $(this).attr("trans-in-id"),
    //         type: "GET",
    //         dataType: "json",
    //     });
         
    //     request.done(function( msg ) {
    //         flash('The trans in is deleted', 'success');
    //     });
         
    //     request.fail(function( jqXHR, textStatus ) {
    //         flash('Deletion failed', 'error');
    //     });
    // });
});

var transInViewView;

$(function() {
    transInViewView = new TransInViewView();

    $(document).on('click', '#new-btn', function() {
        $(this).hide();
        // var associationNewView = new TransInViewView();
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
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#trans-in-view-template').html(),
            {trans_in_list: this.trans_in_list.models});
        $('#trans_in_list tbody').html(template);
    },
    events: {
        'click button.edit': 'edit',
        'click button.remove': 'remove'
    },
    edit: function(event) {
        var $this = $(event.currentTarget);
        var $tr = find_tr($this);
        var id = $tr.data('id');
        var trans_in = trans_in_list.get(id);

        var trans_inEditView = new TransInEditView({model: trans_in,
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
        var trans_in = trans_in_list.get(id);

        trans_in.destroy({
            success: function() {
                clearflash();
                flash('Transaction removed successfully', 'success');

                this.render();
            }, error: function(response) {
                ajax_error_handler(response);
            }
        });
    }
});