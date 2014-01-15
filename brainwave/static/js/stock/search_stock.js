$( document ).ready(function() {
    $('#search_field').bind('input', function() { 
        stock_ajax_search("/api/stock/search/", "#stock_results", "#stock-template", $(this).val());
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
function stock_ajax_search(path, target, template_loc, query){
    var request = $.ajax({
        url: path + query,
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

        for (i = 0; i < msg.stock.length; i++) {
            var stock = msg.stock[i];
            $(target).append(template(stock));
        }
       
    });
     
    request.fail(function( jqXHR, textStatus ) {
        $(target).html("No results");
    });
}