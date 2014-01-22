var TransactionModel = Backbone.Model.extend({
    urlRoot: '/api/transaction',
    defaults: {
        pay_type: 'cash',
        items: ''
    },
    initialize: function(){
        this.bind("error", function(model, error){});
    }
});

var EntryModel = Backbone.Model.extend({
    defaults: {
        product_id: 0,
        quantity: 0,
        action: 'sell'
    },
    initialize: function(){
        this.bind("error", function(model, error){});
    }
});

var EntryCollection = Backbone.Collection.extend({
    model: EntryModel
});

var ProductModel = Backbone.Model.extend({
    initialize: function(){
        this.bind("error", function(model, error){});
    }
});

var Products = Backbone.Collection.extend({
    model: ProductModel
});

var ProductButtonView = Backbone.View.extend({
    products: new Products(),
    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/product/all', {}, function(data) {
            me.products = new Products(data.products);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#productbutton-view-template').html(),
            {products: this.products.models});
        $('#pos-item-container').html(template);
    }
});

var ReceiptView = Backbone.View.extend({
    transaction: new TransactionModel(),
    initialize: function() {
            this.render();
    },
    update: function() {
        $('<li class="list-group-item"><span class="item-count" product-id="' +
            '1' + '">1</span>x 1<span class="badge">' + '2.00' +
            '</span><div class="list-delete">Delete</div></li>').insertAfter('.item-list li:first');
    },
    render: function() {
        $(document).ready(function() {
            var template = _.template($('#receipt-view-template').html());
            $('#receipt').html(template);
        });
        this.update();
        this.update();
    }
});

var product_button_view = new ProductButtonView();
var receipt_view        = new ReceiptView();















$(document).ready(function() {
    var numpad_active = true;

    /* Event handler for numpad buttons */
    $('.numpad-btn').hammer().on('tap', function(e) {
        if (!numpad_active) return;

        /* Animate the tap */
        $(".numpad").find('.numpad-btn').stop(true, true);
        var startColor = '#ffffff';
        var endColor   = $(this).css('background-color');
        $(this).css('background-color', startColor).animate({
            backgroundColor: endColor
        }, 500);

        /* Deal with the actual functionality */
        var inner = $(this).html();
        var val = parseInt($('#numpad-display').html() + inner);
            val = (val > 999) ? 1000 : val;

        if (inner == 'CL') $('#numpad-display').html('');
        else               $('#numpad-display').html(val);
    });
});