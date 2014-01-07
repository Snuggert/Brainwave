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
    urlRoot: '/',
    defaults: function(){
        return{
            name: '',
        };
    }
});

models.Product = Backbone.Model.extend({
    urlRoot: '/',
    defaults: function(){
        return{
            active: null,
            name: '',
            shortname: '',
            price: null,
            volume: null,
            loss: null,
            product_category_id: null,
        };
    }
});

models.Stock = Backbone.Model.extend({
    urlRoot: '/',
    defaults: function(){
        return{
            stock: null,
            stock_type: null,
        };
    }
});