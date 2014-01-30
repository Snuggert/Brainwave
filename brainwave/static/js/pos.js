/* Create an event-bus that allows views to communicate via events */
Backbone.pubSub = _.extend({}, Backbone.Events);

/* Backbone Models */
var TransactionModel = Backbone.Model.extend({
    urlRoot: '/api/transaction',
    defaults: {
        pay_type: 'cash',
        action: 'sell',
        customer_id: 0,
        mutable: true /* This is meta-data, not important to the API */
    },
    initialize: function() {
        /* Set this.entries to a new collection as a default value */
        this.attributes.entries = new EntryCollection();
        /* The comparator function defines the way in which a collection
         * should be sorted. In this case, it's by 'last updated'
         */
        this.attributes.entries.comparator = function(entries) {
            /* Reverse sort the entries collection. Note the minus! */
            return -entries.get('modified_time');
        };
    },
    new_entry: function(data) {
        /* Set the modified_time, which is used for sorting the collection */
        data['modified_time'] = new Date().getTime();
        /* Check if a model for this item already exists in the collection */
        var current = this.get('entries').where({product_id: data.product_id});
        if (current.length) {
            /* Update the model to the appropriate quantity */
            var quantity = current[0].get('quantity') + data.quantity;
            if (quantity <= 0) {
                this.delete_entry(data);
                return;
            }
            current[0].set({'quantity': quantity,
                           'modified_time': data.modified_time});
            /* Force the collection to sort again, which normally only happens
             * on add() */
            this.get('entries').sort();
        } else {
            if (data.quantity <= 0)
                return;
            /* Create a new model in the entries collection */
            this.get('entries').add(new EntryModel(data));
        }
    },
    delete_entry: function(data) {
        var model = this.get('entries').where({product_id: data.product_id});
        this.get('entries').remove(model);
        /* Tell the ProductButtonView to clear the amount on the button */
        Backbone.pubSub.trigger('entry_deleted',
                                {'product_id': data.product_id, 'quantity': 0});
    }
});

var EntryModel = Backbone.Model.extend({
    defaults: {
        product_id: 0,
        quantity: 0,
        price: 0.0, /* price for a single item, not multiplied by quantity */
        modified_time: 0 /* Meta-data, to be used for sorting purposes */
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize an EntryModel.");
        });
        /* If the remove event on the entrycollection is triggered, destroy */
        this.bind("remove", function() {
            this.destroy();
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

var ProductCategory = Backbone.Model.extend({
    defaults: {
        id: 0,
        name: '',
        color: ''
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a ProductCategoryModel.");
        });
    }
});

var CustomerModel = Backbone.Model.extend({
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a CustomerModel.");
        });
    }
});

var PayModuleModel = Backbone.Model.extend({
    defaults: {
        receipt_price: 0.0
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a PayModuleModel.");
        });
    }
});

var OverlayModel = Backbone.Model.extend({
    defaults: {
        status: 'off', /* can also be 'on' */
        message: '',
        quiet: true /* When false, a prompt will show before disappearing */
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a OverlayModel.");
        });
    }
});

var NumpadModel = Backbone.Model.extend({
    defaults: {
        type: 'standard', /* Type of numpad. Can also be 't9' */
        real: 1,
        display: '1'
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a NumpadModel.");
        });
    }
});

TransactButtonModel = Backbone.Model.extend({
    defaults: {
        state: 'pay' /* State of the button, not the page as a whole */
    },
    initialize: function() {
        this.bind("error", function(model, error) {
            console.log("Could not initialize a TransactButtonModel.");
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

var ProductCategories = Backbone.Collection.extend({
    model: ProductCategory
});

var Customers = Backbone.Collection.extend({
    model: CustomerModel,

    /* The search function will take a string of digits and return a new
     * collection, which contains all the models that have names that have t9
     * matches.
     */
    search: function(str) {
        if(str == '') return this;

        var regex = this.regex_make(str);
        /* Make a new collection that holds the filtered results. This is
         * required, lest the list slims down with each iteration and lost
         * elements become unretrievable.
         */
        var filtered = new Customers();
        this.each(function(model) {
            if (regex.test(model.get("name").split(/0|1/).join('')) ||
                regex.test(model.get("name")))
                filtered.add(model);
        });
        return filtered;
    },

    regex_make: function(str) {
        var pattern = '';
        var chars = [" 0", " 1", "ABCÀÁÅÃÆÇàáâãäåæç2", "DEFÈÉÊËèéêë3",
                     "GHIÌÍÎÏìíîï4", "JKL5", "MNOÑñÒÓÔÕÖØòóôõöøð6", "PQRSß7",
                     "TUVÙÚÛÜùúûü8", "WXYZýþÿÝÞ9"];

        for (var i = 0; i < str.length; i++)
            pattern += '[' + chars[parseInt(str[i])] + ']';
        return new RegExp(pattern, "i");
    }
});

/*Backbone Views */
var ProductButtonView = Backbone.View.extend({
    products: new Products(),
    product_categories: new ProductCategories(),
    category_id: 0,
    receiptData: {},
    initialize: function() {
        /* Listen to custom events that are triggered by TransactionView */
        Backbone.pubSub.on('add_entry_finish', this.on_add_entry_finish, this);
        Backbone.pubSub.on('receipt_emptied', this.on_receipt_emptied, this);
        /* Listen to a custom event that is triggered by NumpadView */
        Backbone.pubSub.on('numpad_push', this.on_numpad_push, this);
        /* Listen to a custom event that is triggered by TransactionModel */
        Backbone.pubSub.on('entry_deleted', this.on_entry_deleted, this);
        /* Listen to a custom event that is triggered by CategoryNavbarView */
        Backbone.pubSub.on('category_switch', this.on_category_switch, this);
        this.update();
    },
    hammerEvents: {
        'tap .item-btn': 'prepare_entry'
    },
    update: function() {
        var me = this;

        $.get('/api/product/all', {}, function(data) {
            me.products = new Products(data.products);
            $.get('/api/product_category/all', {}, function(data) {
                me.product_categories = new ProductCategories(
                        data.product_categories);

                _.each(me.products.models, function(product) {
                    product.product_category = me.product_categories.get(
                            product.get('product_category_id'));
                });

                me.render();

                /* The product categories navbar wishes access to the
                 * cateogires. Send them back via a pubSub event.
                 */
                Backbone.pubSub.trigger('categories_push',
                                        me.product_categories);
            });
        });
    },
    render: function() {
        var template = _.template($('#productbutton-view-template').html(),
            {products: this.products.models, category_id: this.category_id});
        this.$el.html(template);

        /* The button overlays have to be sized/shaped with jQuery. */
        $().shape_overlays();
    },
    prepare_entry: function (event) {
        var $this    = $(event.currentTarget)
        ,   id       = parseInt($this.attr("product-id"))
        ,   price    = parseFloat($this.attr("product-price"))
        ,   name     = $this.find('.item-btn-name').text();
        /* Make a JSON object, which shall be passed to TransactionView later. */
        this.receiptData = {'product_id': id, 'price': price, 'name': name};
        /* Trigger a custom event that NumpadView is listening to. This is so
         * the numpad value can be obtained.
         */
        Backbone.pubSub.trigger('numpad_pull');
    },
    send_entry: function(data) {
        this.receiptData['quantity'] = data.value;
        /* Trigger a custom event that TransactionView is listening to */
        Backbone.pubSub.trigger('add_entry_init', this.receiptData);
    },
    set_btn_quantity: function(data) {
        /* Display the quantity of a product on the relevant button.
         * This is not done in the render function, since that would require
         * all buttons to render again. Using jQuery instead.
         */
        var quantity = (data.quantity == 0) ? '' : data.quantity;

        $("div[product-id='" + data.product_id + "'] .item-btn-amount-now")
            .html(quantity);
    },
    clear_buttons: function() {
        $('.item-btn-amount-now').html('');
    },
    on_add_entry_finish: function(data) {
        this.set_btn_quantity(data);
    },
    on_receipt_emptied: function() {
        this.clear_buttons();
    },
    on_numpad_push: function(data) {
        this.send_entry(data);
    },
    on_entry_deleted: function(data) {
        this.set_btn_quantity(data);
    },
    on_category_switch: function(data) {
        this.category_id = data.category_id;
        
        this.$el.find('.col-sm-3').show();
        if (this.category_id > 0)
            this.$el.find('.col-sm-3').not('.product-cat-' + this.category_id).hide();
    }
});

PayModuleView = Backbone.View.extend({
    customers_all: new Customers(),
    paymodule: new PayModuleModel(),

    initialize: function() {
        this.update();
        /* Listen to custom events from the TransactionView */
        Backbone.pubSub.on('pay_init', this.on_pay_init, this);
        Backbone.pubSub.on('pay_complete', this.on_pay_complete, this);
        Backbone.pubSub.on('t9_change', this.on_t9_change, this);
    },
    hammerEvents: {
        'tap .confirm-btn': 'confirm',
        'tap .list-group-item': 'select_customer',
        'tap .customer-list .list-group-item:first-child > span': 'show_new_customer'

    },
    update: function() {
        var me = this;

        $.get('/api/customer/all', {}, function(data) {
            me.customers_all = new Customers(data.customers);
            me.filter('');
            me.render();
        });
    },
    filter: function(str) {
        this.customers_few = this.customers_all.search(str);
    },
    render: function() {
        var template = _.template($('#customer-view-template').html(),
            {customers: this.customers_few.models});
        this.$el.html(template);
    },
    confirm: function(event) {
        var $this  = $(event.currentTarget);

        if ($this.hasClass('cash'))
            var pay_type = 'cash'
        else if ($this.hasClass('pin'))
            var pay_type = 'pin'
        else if ($this.hasClass('credit') && !$this.hasClass('grayed'))
            var pay_type = 'credit'
        else
            return;

        var customer_id = parseInt($('.customer-list').find('.selected').
                                   attr('customer-id'));

        var jsonData = {'pay_type': pay_type, 'customer_id': customer_id};
        Backbone.pubSub.trigger('pay', jsonData);
    },
    select_customer: function(event) {
        var $this  = $(event.currentTarget);

        var current_id = $('.customer-list .selected').attr('customer-id');
        this.unselect_customer();
        /* Only add a new class if a different customer was tapped. Otherwise,
         * it is supposed to work like a toggle.
         */
        if (($this.attr('customer-id') != current_id ||
             $this.attr('customer-id') == -1) &&
             ($this.attr('customer-id') > 0 ||
              $this.attr('customer-id') == -1)) {
            $this.addClass('selected');
            this.$el.find('.credit').removeClass('grayed');
        }
    },
    unselect_customer: function() {
        $('.customer-list .selected').removeClass('selected');
        this.$el.find('.credit').addClass('grayed');
    },
    show_new_customer: function(event) {
        me = this;

        /* Show all customers from all associations */
        $.get('/api/customer/all/all', {}, function(data) {
            me.customers_all = new Customers(data.customers);
            me.filter('');
            me.render();
    
            /* Show the input bar and hide the add button */
            $('.customer-list .list-group-item:nth-child(2)').slideDown();
            $('.customer-list .list-group-item:first-child > span').hide();
            /* Now put the selected class on the li element */
            $('.customer-list .list-group-item:nth-child(2)').addClass('selected');
            event.stopPropagation();
            /* Add focus to input field */
            $('.customer-list .list-group-item:nth-child(2) > input').focus();
        });

    },
    on_pay_init: function(data) {
        this.paymodule.set({'receipt_price': data.receipt_price});
        this.unselect_customer();
        this.filter('');
        this.render();
    },
    on_pay_complete: function(data) {
        this.update();
    },
    on_t9_change: function(data) {
        this.filter(data.value);
        this.render();
    }
});

OverlayView = Backbone.View.extend({
    overlay: new OverlayModel(),
    initialize: function() {
        /* Listen to custom events from the TransactionView */
        Backbone.pubSub.on('pay', this.on_pay, this);
        Backbone.pubSub.on('pay_complete', this.on_pay_complete, this);
        Backbone.pubSub.on('pay_cancel', this.on_pay_cancel, this);
    },
    hammerEvents: {
        'tap .confirm-btn': 'confirm'
    },
    show: function(loading) {
        if (loading) {
            this.$el.find('.confirm-btn').hide();
            this.$el.find('#loading-img').show();
            this.overlay.set({'message': 'Processing..'});
        } else {
            this.$el.find('.confirm-btn').show();
            this.$el.find('#loading-img').hide();
        }

        this.$el.find('#overlay-msg').html(this.overlay.get('message'));
        this.$el.show();
    },
    hide: function() {
        this.overlay.set({'message': ''});
        this.$el.hide();
    },
    confirm: function() {
        this.hide();
    },
    on_pay: function() {
        this.show(true);
    },
    on_pay_complete: function() {
        this.hide();
    },
    on_pay_cancel: function(data) {
        if (data && data.reason == 'error') {
            var obj = $.parseJSON(data.message);
            this.overlay.set({'message': obj.error});
            this.show(false);
        } else
            this.$el.hide();
    }
});

var TransactionView = Backbone.View.extend({
    transaction: new TransactionModel(),
    initialize: function() {
        /* Listen to custom events from the ProductButtonView */
        Backbone.pubSub.on('add_entry_init', this.on_add_entry_init, this);
        Backbone.pubSub.on('entry_deleted', this.on_entry_deleted, this);
        /* Listen to custom events from the PayButtonView */
        Backbone.pubSub.on('pay_init_request', this.on_pay_init_request, this);
        Backbone.pubSub.on('pay_init', this.on_pay_init, this);
        Backbone.pubSub.on('pay', this.on_pay, this);
        /* Listen to a custom event that can come from multiple places */
        Backbone.pubSub.on('pay_cancel', this.on_pay_cancel, this);
        /* Start a new transaction and render an empty list */
        this.empty();
    },
    hammerEvents: {
        'swipeleft .list-group-item': 'show_delete',
        'tap .list-group-item': 'hide_delete',
        'tap .list-delete': 'delete_entry'
    },
    empty: function() {
        this.transaction = new TransactionModel();
        this.render();

        Backbone.pubSub.trigger('receipt_emptied', {});
    },
    lock: function() {
        this.transaction.set({'mutable': false});
    },
    unlock: function() {
        this.transaction.set({'mutable': true});
    },
    is_locked: function() {
        return !this.transaction.get('mutable');
    },
    render: function() {
        var template = _.template($('#receipt-view-template').html(),
            {entries: this.transaction.get('entries').models});
        this.$el.html(template);

        var total = this.get_total();
        /* Set the receipt total. For now, this is done using jQuery, since
         * the total price is not a part of any model.
         */
        $('#receipt-total').text(total.toFixed(2).replace('.', ','));

        if (total) {
            /* Now pass some data to the ProductButtonView, so it can reset the
             * amount displayed on the appropriate button. A custom event is
             * triggered to facilitate this.
             */
            var latest = this.transaction.get('entries').models[0].attributes;
            var jsonData = {'product_id': latest.product_id,
                            'quantity': latest.quantity};
            Backbone.pubSub.trigger('add_entry_finish', jsonData);
        }
    },
    get_total: function() {
        var total = 0.0;
        _.each(this.transaction.get('entries').models, function(entry) {
            total += (entry.get('price') * entry.get('quantity'));
        });
        return total;
    },
    new_entry: function(data) {
        if (this.is_locked())
            return;

        /* Add a new entryModel to the collection in the transaction model */
        this.transaction.new_entry(data);
        this.render();

        /* Scroll to top of the receipt */
        this.$el.scrollTop(0);
    },
    delete_entry: function(event) {
        if (this.is_locked())
            return;

        var $this  = $(event.currentTarget)
        ,   id     = $this.parent().find('.item-count').attr('product-id');

        if ($this.hasClass('list-delete-all'))
            this.empty();
        else
            this.transaction.delete_entry({'product_id': parseInt(id)});
    },
    pay: function(data) {
        var me = this;

        if(!this.transaction.get('entries').length)
            return;

        /* THe data.customer_new attribute should be filled when a new customer
         * should be added to the database. This will be handled by the 
         * transaction api.
         */
        data.customer_new = '';
        if (data.customer_id == -1)
            data.customer_new = $('#new-customer-field').val();

        this.transaction.set({'pay_type': data.pay_type,
                              'customer_id': data.customer_id,
                              'customer_new': data.customer_new});

        this.transaction.save({}, {
            success: function() {
                me.empty();
                Backbone.pubSub.trigger('pay_complete', {});
            }, error: function(model, response) {
                Backbone.pubSub.trigger('pay_cancel',
                                        {'reason': 'error',
                                         'message': response.responseText});
            }
        });
    },
    hide_delete: function() {
        /* Hide all delete buttons */
        $('.list-delete').hide();
    },
    show_delete: function(event) {
        if (this.is_locked())
            return;

        var $this = $(event.currentTarget);
        /* Hide all delete buttons */
        this.hide_delete();
        /* Scale the button and show it with a slide */
        $this.find('.list-delete').css('line-height',
                $this.find('.list-delete').height() + 'px');
        $this.find('.list-delete').show('slide', {direction: 'right'}, 250);
    },
    on_add_entry_init: function(data) {
        this.new_entry(data);
    },
    on_entry_deleted: function(data) {
        this.render(data);
    },
    on_pay_init_request: function(data) {
        /* Verify that the receipt isn't empty */
        if (this.get_total() > 0.0)
            Backbone.pubSub.trigger('pay_init_allowed',
                                    {'receipt_price': this.get_total()});
    },
    on_pay_init: function(data) {
        /* Lock the receipt, so it can no longer be modified */
        this.lock();

        /* Hide all delete buttons */
        this.hide_delete();
    },
    on_pay: function(data) {
        this.pay(data);
    },
    on_pay_cancel: function(data) {
        this.unlock();
    }
});

var NumpadView = Backbone.View.extend({
    numpad: new NumpadModel(),
    initialize: function() {
        /* Listen to custom events from the ProductButtonView */
        Backbone.pubSub.on('numpad_pull', this.on_numpad_pull, this);
        Backbone.pubSub.on('pay_init', this.on_pay_init, this);
        /* Listen to a custom event from the PayModuleView */
        Backbone.pubSub.on('pay', this.on_pay, this);
        /* Listen to a custom event that can come from multiple places */
        Backbone.pubSub.on('pay_cancel', this.on_pay_cancel, this);
        /* Listen to a custom event from the TransactionView */
        Backbone.pubSub.on('receipt_emptied', this.on_receipt_emptied, this);
        /* Set the numpad to a default value */
        this.hard_reset();
    },
    hammerEvents: {
        'tap .numpad-btn': 'tapped'
    },
    hard_reset: function() {
        /* This function does the same as reset, only also forces the numpad
         * back to the standard type.
         */
        this.numpad.set({'type': 'standard'});
        this.reset();
    },
    reset: function() {
        if (this.numpad.get('type') == 'standard') {
            this.numpad.set({'display': '', 'real': 1});
            $('#numpad-ctrl-sign').text('Neg (-)');
        }
        else if (this.numpad.get('type') == 't9') {
            this.numpad.set({'display': '', 'real': ''});
            $('#numpad-ctrl-sign').text('<=');
        }
        this.display();
    },
    render: function() {
        /* This is temporary, the numpad should be rendered via lodash.js */
        this.display();
    },
    display: function() {
        $('#numpad-display').html(this.numpad.get('display'));
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
        var numpad_id = $this.attr('numpad-id');

        /* If the ctrl button was tapped, call another function. */
        if (numpad_id == 'ctrl' && this.numpad.get('type') == 'standard')
            this.invert_sign();
        else if (numpad_id == 'ctrl' && this.numpad.get('type') == 't9')
            this.backspace();
        else if (numpad_id == 'cl')
            this.reset();
        else {
            var val = $('#numpad-display').html() + numpad_id;
            if (this.numpad.get('type') == 'standard') {
                val = parseInt(val);
                val = (val > 999)  ? 1000 :
                      (val < -999) ? -1000 : val;
            }
            
            this.numpad.set({'display': val.toString(), 'real': val});
            this.display();
        }

        /* If the numpad is set to t9, trigger an event so the customer list
         * can be re-rendered
         */
        if (this.numpad.get('type') == 't9') {
            var jsonData = {'value': this.numpad.get('display')};
            Backbone.pubSub.trigger('t9_change', jsonData);
        }
    },
    invert_sign: function() {
        var current = this.numpad.get('display');

        display = (current == '') ? '-' :
                  (current == '-') ? '' : -1 * current;
        real    = (current == '') ? -1 :
                  (current == '-') ? 1 : -1 * current;
               
        this.numpad.set({'display': display.toString(), 'real': real});
        this.render();

        /* Toggle the value of the invert button */
        $('#numpad-ctrl-sign').text((real < 0) ? 'Pos (+)' : 'Neg (-)');
    },
    backspace: function() {
        var str = this.numpad.get('display').slice(0, -1);
        this.numpad.set({'display': str, real: str});
        /* Now display the new value */
        this.display();
    },
    on_pay_init: function() {
        this.numpad.set({'type': 't9'});
        $('#numpad-ctrl-sign').text('<=');
        this.reset();
    },
    on_pay_cancel: function() {
        this.hard_reset();
    },
    on_pay: function() {
        this.hard_reset();
    },
    on_receipt_emptied: function() {
        /* This is indirectly called by pay_complete event, via TransactionView */
        this.hard_reset();
    },
    on_numpad_pull: function() {
        /* Get the numpad value and trigger an event for ProductButtonView */
        var jsonData = {'value': this.numpad.get('real')};
        Backbone.pubSub.trigger('numpad_push', jsonData);

        /* Reset the numpad value to 1 and render again */
        this.reset();
    }
});

var TransactButtonView = Backbone.View.extend({
    button: new TransactButtonModel(),
    initialize: function() {
        this.button.set({'status': 'pay'});
        /* Listen to custom events that can come from different views */
        Backbone.pubSub.on('pay_init_allowed', this.on_pay_init_allowed, this);
        Backbone.pubSub.on('pay_init', this.on_pay_init, this);
        Backbone.pubSub.on('pay_cancel', this.on_pay_cancel, this);
        Backbone.pubSub.on('pay_complete', this.on_pay_complete, this);
    },
    hammerEvents: {
        'tap': 'tapped'
    },
    tapped: function(event) {
        if (this.button.get('status') == 'pay')
            /* Ask the TransactionView if there are any products to be sold */
            Backbone.pubSub.trigger('pay_init_request');
        else if (this.button.get('status') == 'cancel')
            Backbone.pubSub.trigger('pay_cancel');
    },
    toggle: function() {
        this.$el.toggleClass("pay-btn cancel-btn");
        $('.transact-btn-text').text((this.button.get('status') == 'pay') ? 'Cancel' : 'Pay');
        this.button.set({'status':   (this.button.get('status') == 'pay') ? 'cancel' : 'pay'});
        /* Toggle the views */
        $().toggle_views();
    },
    on_pay_init_allowed: function(data) {
        /* Show the pay module */
        Backbone.pubSub.trigger('pay_init', data);
    },
    on_pay_init: function() {
        this.toggle();
    },
    on_pay_cancel: function() {
        this.toggle();
    },
    on_pay_complete: function() {
        this.toggle();
    }
});


var CategoryNavbarView = Backbone.View.extend({
    initialize: function() {
        Backbone.pubSub.on('categories_push', this.on_categories_push, this);
    },
    hammerEvents: {
        'tap li': 'tapped'
    },
    render: function() {
        var template = _.template($('#product-cat-view-template').html(),
            {categories: this.product_categories.models});
        this.$el.html(template);
    },
    tapped: function(event) {
        var $this = $(event.currentTarget)
        ,   id    = $this.attr('cat-id');

        /* Remove current focus class at the relevant list element */
        $this.parent().find('.focus').removeClass('focus');
        /* Add focus to this element */
        $this.addClass('focus');

        /* Tell the ProductButtonView to render the appropriate buttons */
        Backbone.pubSub.trigger('category_switch', {category_id: id});
    },
    on_categories_push: function(data) {
        this.product_categories = data;
        this.render();
    }
});


$(document).ready(function() {
    /* Initialize the backbone views */
    var product_button_view  = new ProductButtonView({ el: $("#pos-item-container") });
    var pay_module_view      = new PayModuleView({ el: $("#pos-pay-container") });
    var overlay_view         = new OverlayView({ el: $(".overlay") });
    var receipt_view         = new TransactionView({ el: $("#receipt") });
    var numpad_view          = new NumpadView({ el: $("#numpad") });
    var transact_button_view = new TransactButtonView({ el: $(".transact-btn") });
    var cat_navbar_view      = new CategoryNavbarView({ el: $(".nav-categories") });

    /* Event handler for window resize, which resizes the item-btn overlays */
    $(window).on('resize', function(e) {
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

$.fn.toggle_views = function () {
    $('#pos-item-container').toggle();
    $('#pos-pay-container').toggle();
}
