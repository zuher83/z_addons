odoo.define('z_backend_theme.List', function (require) {
    "use strict";

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');


    ListRenderer.include({
        _renderBodyCell: function (record, node, colIndex, options) {
            var $res = this._super.apply(this, arguments);
            if (node.tag === 'field') {
                var typeClass = this.state.fields[node.attrs.name].type;
                if (typeClass === 'monetary' || typeClass === 'float') {
                    var curField = this.state.fields[node.attrs.name];
                    var curFieldVal = record.data[node.attrs.name];

                    if ((!curFieldVal > 0) || (!curFieldVal < 0)) {
                        $res.addClass('oe_null_zero_number');
                    }
                }
            }
            return $res;
        },
    });
});
