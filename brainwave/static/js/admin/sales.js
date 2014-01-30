$(document).ready(function () {
    $('.to_date, .from_date').each(function () {
        $(this).datepicker({
            format: "dd-mm-yyyy",
            autoclose: true,
        });

        $(this).datepicker('update', new Date());
    });

	$( ".to_date" ).change(function() {
		var to_date = $(this).val();
		var from_date = $(".from_date").val();
		get_sales(from_date, to_date, '#products_filtered_results', '#sales-template');
	});

	$( ".from_date" ).change(function() {
		var from_date = $(this).val();
		var to_date = $(".to_date").val();
		get_sales(from_date, to_date, '#products_filtered_results', '#sales-template');
	});

});


/**
 * Call a search api call and put them in the results.
 *
 * @param path Path to the api service.
 * @param target Target to append the list to
 * @param template_loc Indentifier of the template
 * @param query search string
 */
function get_sales(from_date, to_date, target, template_loc){
    var request = $.ajax({
        url: '/api/transaction/sales/' + from_date + '/' + to_date,
        type: "GET",
        dataType: "json",
    });
     
    request.done(function( msg ) {
        console.log(msg);
        if( msg.error !== undefined){
            $(target).html("No results");
            return false;
        }

        var template = _.template($(template_loc).html());

        $(target).html("");

        $.each(msg.transaction, function() {
        	console.log(this);
        	$(target).append(template({pricesum:this.pricesum, 
        					           quantitysum:this.quantitysum,
        					       	   name: this.name}));
		});
    });
     
    request.fail(function( jqXHR, textStatus ) {
        $(target).html("No results");
    });
}