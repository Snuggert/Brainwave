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
            color: '',
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
            quantity: null,
            unit: 'amount',
            direct: true,
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
            name: null,
            direct: null,
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
    defaults: {id: null, name: ''},
    initialize: function() {
        var me = this;

        this.associations = new collections.Associations();
        this.associations.url = function() {
            return me.urlRoot + '/association/' + me.get('id');
        };
    }
});

models.Trans_in = Backbone.Model.extend({
    urlRoot: '/api/trans_in',
    defaults: function() {
        return {
            price: null,
            quantity: null,
            stock_id: null,
            in_stock: true,
        };
    }
});

/* Collections. */
var collections = {};

collections.Associations = Backbone.Collection.extend({
    model: models.Association,
    url: '/api/association/all',
    parse: function(response) {
        return response.associations;
    }
});

collections.ProductCategories = Backbone.Collection.extend({
    model: models.ProductCategory,
    url: 'api/product_category/all',
    parse: function(response){
        return response.product_categories
    }
})

collections.Trans_in_list = Backbone.Collection.extend({
    model: models.Trans_in
});

collections.Customers = Backbone.Collection.extend({
    model: models.Customer
});

collections.Stocks = Backbone.Collection.extend({
    model: models.Stock,
    url: 'api/stock/all',
    parse: function(response){
        return response.stocks
    }
});

collections.Users = Backbone.Collection.extend({
    model: models.User
});
