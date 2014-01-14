'use strict';

$(function(){
    $('select').select2();
    var $button;
    $('button.remove').on("click", function(event){
        $button = $(this);
        $('div#remove_modal').modal('show')
        $.each(brainwave.products, function( key, value ) {
            if(value.id == $button.attr('data-id')){
                $('div#remove_modal').find('div.modal-body').html(value.name)
                $('div#remove_modal').find('button.finalremove').attr('data-id', value.id)
            }
        });
    });
    $('button.finalremove').on("click", function(event){
        $button = $(this);
        $.ajax({
            type: "DELETE",
            url: "/api/product/" + $button.attr('data-id'),
            }).success(function(msg) {
                clearflash();
                flash('Het product is verwijderd', 'success');
        });
    });
})