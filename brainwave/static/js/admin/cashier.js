

$(document).ready(function () {
	$(document).on('click', '#send_cash', function(e) {
		var amount = $("#cash").val();
		console.log(amount);
		$("#cash").val("");
		change_cash(amount, "#cash_amount");
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
function change_cash(amount, target){
    var request = $.ajax({
        url: '/api/association/cash_counter/set/' + amount,
        type: "GET",
        dataType: "json",
    });
     
    request.done(function( msg ) {
        console.log(msg);
        update_cash(target);
    });
     
    request.fail(function( jqXHR, textStatus ) {
        $(target).html("No results");
    });
}

function update_cash(target){
    var request = $.ajax({
        url: '/api/association/cash_counter/get',
        type: "GET",
        dataType: "json",
    });
     
    request.done(function( msg ) {
    	console.log(msg);
    	$(target).html("Cash: €" + msg.cash_counter);
    });
     
    request.fail(function( jqXHR, textStatus ) {
        $(target).html("No results");
    });
}