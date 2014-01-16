/* Backbone stuff. */
associations = new collections.Associations(brainwave.associations);

var $field_view = $('.field-view');
var $field_edit = $('.field-edit');

/* Hide inline edit fields. */
$field_edit.hide();

/* Reset old values. */
function reset_old_vals($tr) {
    var orig_name = $tr.find('td[data-property=name]').text();
    $tr.find('input[data-property=name]').val(orig_name);
}

/* What happens when the edit button is clicked. */
$('.edit').click(function() {
    // Hide view td's, show edit td's.
    $field_view.hide();
    $field_edit.show();
});

/* What happens when the save button is clicked. */
$('.save').click(function() {
    var $tr = find_tr($(this));
    var id = $tr.data('id');
    var association = associations.get(id);

    set_form_values(association, $tr);
    association.save({}, {
        success: function() {
            clearflash();
            flash('Association saved successfully', 'success');
        }, error: function(response) {
            ajax_error_handler(response);
            reset_old_vals($tr);
        }
    });

    $tr.find('td[data-property=name]').text(association.get('name'));

    // Hide edit td's, show view td's.
    $field_view.show();
    $field_edit.hide();
});

/* What happens when the cancel button is clicked. */
$('.cancel').click(function() {
    var $tr = find_tr($(this));

    // Reset field value.
    reset_old_vals($tr);

    // Hide edit td's, show view td's.
    $field_view.show();
    $field_edit.hide();
});

/* What happens when the remove button is clicked. */
$('.remove').click(function() {
    var $this = $(this);

    var id = $this.parents('tr').data('id');

    // TODO Actually remove the association.
});

var $new_assoc_btn = $('#new-association>button');
var $new_assoc_form = $('#new-association>div#new-association-form');

/* Hide new association form. */
$new_assoc_form.hide();

/* What happens when the new association button is clicked. */
$new_assoc_btn.click(function() {
    // Hide button, show form.
    $new_assoc_btn.hide();
    $new_assoc_form.show();
});

/* What happens when the new association save button is clicked. */
$('#save-new-association').click(function() {
    // TODO Actually save the association.

    // Show button, hide form. (Later only on success)
    $new_assoc_btn.show();
    $new_assoc_form.hide();
});

/* What happens when the new association cancel button is clicked. */
$('#cancel-new-association').click(function() {
    // TODO Reset form fields.

    // Show button, hide form.
    $new_assoc_btn.show();
    $new_assoc_form.hide();
});
