$( document ).ready(function() {
    $('#search_field').bind('input', function() { 
        product_ajax_search("/api/product/search/", "#product_results", "#product-template", $(this).val());
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
function product_ajax_search(path, target, template_loc, query){
    var request = $.ajax({
        url: path + query,
        type: "GET",
        dataType: "json",
    });
     
    request.done(function( msg ) {
        if( msg.error !== undefined){
            $(target).html("No results");
            return false;
        }

        var template = _.template($(template_loc).html());

        $(target).html("");

        for (i = 0; i < msg.products.length; i++) {
            var products = msg.products[i];
            console.log(template(products));
            $(target).append(template(products));
        }
       
    });
     
    request.fail(function( jqXHR, textStatus ) {
        $(target).html("No results");
    });
}