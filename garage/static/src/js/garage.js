openerp.garage = function(instance, local){
	var _t = instance.web._t,
	_lt = instance.web._lt;
	var Qweb = instance.web.qweb;
	local.RtoRegNo = instance.web.form.AbstractField.extend({
		init: function(field_manager, node){
			this._super.apply(this, arguments);
			this.set("value", "");
		},
		render_value: function() {
	        if (this.get("effective_readonly")) {
	            this.$el.text(this.get("value"));
	        } else {
	            this.$("input").val(this.get("value"));
	        }
    	},
		start: function() {
	        this.on("change:effective_readonly", this, function() {
	            this.display_field();
	            this.render_value();
	        });
	        this.display_field();
	        return this._super();
    	},
    	display_field: function() {
	        var self = this;
	        this.$el.html(Qweb.render("reg_no", {widget: this}));
	        if (! this.get("effective_readonly")) {
	            this.$("input").change(function() {
	                self.internal_set_value(self.$("input").val());
	            });
	        }
    	},
		get_value:function(){
			this._super();
		},
		is_valid: function(){
			
			var re = /^([a-zA-Z]){2}[\s]*\d{2}[\s]*([a-zA-z]){2}[\s]*\d{1,4}$/;
			var ok = re.test(this.get('value'))
			if(ok){
				return true;
			}else {
				return false;
			}
		},
	});

instance.web.form.widgets.add('RtoRegNo', 'instance.garage.RtoRegNo');
}