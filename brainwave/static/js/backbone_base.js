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

/* Collections. */
var collections = {};

collections.Associations = Backbone.Collection.extend({
    model: models.Association
});
