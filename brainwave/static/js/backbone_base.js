var models = {};

models.User = Backbone.Model.extend({
    urlRoot: '/',
    defaults: function(){
        return{
            username: '',
        };
    }
});

models.ProductCategory = Backbone.Model.extend({
    urlRoot: '/api/product_category',
    defaults: function(){
        return{
            name: '',
        };
    }
});

models.Product = Backbone.Model.extend({
    urlRoot: '/api/product',
    defaults: function(){
        return{
            name: '',
            shortname: '',
            price: null,
            volume: null,
            product_category_id: null,
            stock_id: null,
            assoc_id: null,
        };
    }
});

models.Stock = Backbone.Model.extend({
    urlRoot: '/api/stock',
    defaults: function(){
        return{
            id: null,
            stock: null,
            stock_type: null,
        };
    }
});

models.Association = Backbone.Model.extend({
    urlRoot: '/api/association',
    defaults: function() {
        return {
            name: '',
        };
    }
});

models.Customer = Backbone.Model.extend({
    urlRoot: '/api/customer',
    defaults: function() {
        return {
            name: '',
        };
    }
});

models.Trans_in = Backbone.Model.extend({
    urlRoot: '/api/trans_in',
    defauts: function() {
        return {
            price: null,
            volume: null,
            in_stock: null,
            stock_id: null,
        };
    }
});

/* Collections. */
var collections = {};

collections.Associations = Backbone.Collection.extend({
    model: models.Association
});

collections.Trans_in_list = Backbone.Collection.extend({
    model: models.Trans_in
});

collections.Customers = Backbone.Collection.extend({
    model: models.Customer
});

collections.Stocks = Backbone.Collection.extend({
    model: models.Stock
});

collections.Users = Backbone.Collection.extend({
    model: models.User
});
