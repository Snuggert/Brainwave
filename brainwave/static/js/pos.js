/* Create an event-bus that allows views to communicate via events */
Backbone.pubSub = _.extend({}, Backbone.Events);

/* Backbone Models */
var TransactionModel = Backbone.Model.extend({
    urlRoot: '/api/transaction',
    defaults: {
        pay_type: 'cash'
    },
    initialize: function() {
        /* Set this.entries to a new collection as a default value */
        this.attributes.entries = new EntryCollection();
        this.attributes.entries.comparator = function(entries) {
            /* Reverse sort the entries collection. Note the minus! */
            return -entries.get("modified_time");
        };
        this.bind("error", function(model, error) {
            console.log("Could not initialize a transaction.");
        });
    },
    new_entry: function(data) {
        /* Set the modified_time, which is used for sorting the collection */
        data['modified_time'] = new Date().getTime();
        /* Check if a model for this item already exists in the collection */
        var current = this.get('entries').where({product_id: data.product_id});
        if (current.length) {
            /* Update the model to the appropriate quantity */
            current[0].set({'quantity': current[0].get('quantity') +
                           data.quantity,
                           'modified_time': data.modified_time});
            /* Force the collection to sort again, which normally only happens
             * on add() */
            this.get('entries').sort();
        } else
            /* Create a new model in the entries collection */
            this.get('entries').add(new EntryModel(data));
   }
});

var EntryModel = Backbone.Model.extend({
    defaults: {
        product_id: 0,
        quantity: 0,
        price: 0.0, /* price for a single item, not multiplied by quantity */
        action: 'sell',
        modified_time: 0 /* Meta-data, to be used for sorting purposes */
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize an EntryModel.");
        });
    }
});

var ProductModel = Backbone.Model.extend({
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a ProductModel.");
        });
    }
});

var NumpadModel = Backbone.Model.extend({
    defaults: {
        value: 1
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a NumpadModel.");
        });
    }
});

/* Backbone Collections */
var EntryCollection = Backbone.Collection.extend({
    model: EntryModel
});

var Products = Backbone.Collection.extend({
    model: ProductModel
});

/*Backbone Views */
var ProductButtonView = Backbone.View.extend({
    products: new Products(),
    receiptData: {},
    initialize: function() {
        /* Listen to a custom event that is triggered by ReceiptView */
        Backbone.pubSub.on('rcpt_done', this.btn_quantity, this);
        /* Listen to a custom event that is triggered by NumpadView */
        Backbone.pubSub.on('send_numpad_val', this.send_to_receipt, this);
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
        this.$el.html(template);

        /* The button overlays have to be sized/shaped with jQuery. */
        $().shape_overlays();
    },
    events: {
        'click .item-btn': 'prepare_to_receipt'
    },
    prepare_to_receipt: function (event) {
        var $this    = $(event.currentTarget)
        ,   id       = parseInt($this.attr("product-id"))
        ,   price    = parseFloat($this.attr("product-price"))
        ,   name     = $this.find('.item-btn-name').text();
        /* Make a JSON object, which shall be passed to ReceiptView later. */
        this.receiptData = {'product_id': id, 'price': price, 'name': name};
        /* Trigger a custom event that NumpadView is listening to. This is so
         * the numpad value can be obtained.
         */
        Backbone.pubSub.trigger('request_numpad_val');
    },
    send_to_receipt: function(data) {
        this.receiptData['quantity'] = data.value;
        /* Trigger a custom event that ReceiptView is listening to */
        Backbone.pubSub.trigger('rcpt_new', this.receiptData);
    },
    btn_quantity: function(data) {
        /* Display the quantity of a product on the relevant button.
         * This is not done in the render function, since that would require
         * all buttons to render again. Using jQuery instead.
         */
        var quantity = (data.quantity == 0) ? '' : data.quantity;

        $("div[product-id='" + data.product_id + "'] .item-btn-amount-now")
            .html(quantity);
    }
});

var ReceiptView = Backbone.View.extend({
    transaction: new TransactionModel(),
    initialize: function() {
        /* Listen to a custom event from the ProductButtonView */
        Backbone.pubSub.on('rcpt_new', this.new_entry, this);
        /* Start a new transaction and render an empty list */
        this.empty();
    },
    empty: function() {
        this.transaction = new TransactionModel();
        this.render();
    },
    render: function() {
        var template = _.template($('#receipt-view-template').html(),
            {entries: this.transaction.get('entries').models});
        this.$el.html(template);

        /* Set the receipt total. For now, this is done using jQuery, since
         * the total price is not a part of any model.
         */
        var total = 0.0;
        _.each(this.transaction.get('entries').models, function(entry) {
            total += (entry.get('price') * entry.get('quantity'));
        });
        $('#receipt-total').text(total.toFixed(2).replace('.', ','));

        if (total) {
            /* Now pass some data to the ProductButtonView, so it can reset the
             * amount displayed on the appropriate button. A custom event is
             * triggered to facilitate this.
             */

            var latest = this.transaction.get('entries').models[0].attributes;
            var jsonData = {'product_id': latest.product_id,
                            'quantity': latest.quantity};
            Backbone.pubSub.trigger('rcpt_done', jsonData);
        }
    },
    new_entry: function(data) {
        /* Add a new entryModel to the collection in the transaction model */
        this.transaction.new_entry(data);
        this.render();
    },
    delete: function(product_id) {

    }
});

var NumpadView = Backbone.View.extend({
    numpad: new NumpadModel(),
    initialize: function() {
        /* Listen to a custom event from the ProductButtonView */
        Backbone.pubSub.on('request_numpad_val', this.push_value, this);
        /* Set the numpad to a default value */
        this.reset();
    },
    reset: function() {
        this.numpad.set({'value': 1});
        this.render(false);
    },
    render: function(manual) {
        /* This render function isn't working with underscore yet. */
        if (!manual)
            /* This means the numpad was just reset, so whilst the value
             * is 1. the numpad display should remain empty.
             */
            $('#numpad-display').html('');
        else
            $('#numpad-display').html(this.numpad.get('value'));
    },
    events: {
        'click .numpad-btn': 'tapped'
    },
    tapped: function(event) {
        var $this = $(event.currentTarget);

        /* Animate the tap */
        $(".numpad").find('.numpad-btn').stop(true, true);
        var startColor = '#ffffff';
        var endColor   = $this.css('background-color');
        $this.css('background-color', startColor).animate({
            backgroundColor: endColor
        }, 500);

        /* Deal with the actual functionality */
        var inner = $this.html();
        var val = parseInt($('#numpad-display').html() + inner);
            val = (val > 999 && inner != 'CL') ? 1000 :
                                                 ((inner == 'CL') ? '' : val);

        this.numpad.set({'value': val});

        this.render(true);
    },
    push_value: function() {
        /* Get the numpad value and trigger an event for ProductButtonView */
        var jsonData = {'value': this.numpad.get('value')};
        Backbone.pubSub.trigger('send_numpad_val', jsonData);

        /* Reset the numpad value to 1 and render again */
        this.numpad.set({'value': 1});
        this.render(false);
    }
});


$(document).ready(function() {
    /* Initialize the backbone views */
    var product_button_view = new ProductButtonView({ el: $("#pos-item-container") });
    var receipt_view        = new ReceiptView({ el: $("#receipt") });
    var numpad_view         = new NumpadView({ el: $("#numpad") });

    /* Event handler for window resize, which resizes the item-btn overlays */
    $(document).on('resize', function(e) {
        $().shape_overlays();
    });
});

/* Here's a custom function that sizes the product overlays (which hold the
 * product amounts) to the size of their parent (which can't be done with
 * css, as the overlays are set to position: absolute)
*/
$.fn.shape_overlays = function () {
    $('.item-btn-amount-now').each(function(index) {
        $(this).width($(this).parent().width() + 'px');
        $(this).outerHeight($(this).parent().outerHeight() + 'px');
        var offset = ($(this).outerHeight() - 75) / 2;
        $(this).css('padding-top', offset + 'px');
    });
}
