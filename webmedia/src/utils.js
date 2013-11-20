if (typeof xmltool === 'undefined') {
    /*jshint -W020 */
    xmltool = {};
}


(function($, ns){
    var re_split = new RegExp('^(.*):([^:]+)$');

    var ATTRNAMES = ['name', 'id', 'class', 'value'];
    var DATANAMES = ['id', 'comment-name', 'target'];

    ns.utils = {
        escape_id: function(id){
            return id.replace(/:/g, '\\:');
        },
        get_prefix: function(id){
            return id.replace(re_split, '$1');
        },
        get_index: function(id){
            return parseInt(id.replace(re_split, '$2'), 10);
        },
        _attr: function(elt, name, value){
            if(typeof value === 'undefined'){
                return elt.attr(name);
            }
            else{
                elt.attr(name, value);
            }
        },
        _data: function(elt, name, value){
            if(typeof value === 'undefined'){
                return elt.data(name);
            }
            else{
                elt.data(name, value);
            }
        },
        _increment_id: function(prefix, elt, func, names, diff){
            // TODO: Perhaps we might support empty prefix
            var re_id = new RegExp('^'+prefix+':(\\d+)');
            for (var key in names){
                var name = names[key];
                var value = func(elt, name);
                if(value){
                    var values = value.split(' ');
                    var output = [];
                    for(var i=0; i<values.length; i++){
                        var v = values[i];
                        var index = parseInt(v.replace(re_id, '$1'), 10);
                        var re = new RegExp('^'+prefix+':'+index);
                        var new_value = v.replace(re, prefix + ':' + (index+diff));
                        output.push(new_value);
                    }
                    func(elt, name, output.join(' '));
                }
            }
        },
        increment_id: function(prefix, elts){
            for (var i=0; i< elts.length; i++){
                var elt = $(elts[i]);
                ns.utils._increment_id(prefix, elt, ns.utils._attr, ATTRNAMES, 1);
                ns.utils._increment_id(prefix, elt, ns.utils._data, DATANAMES, 1);
                ns.utils.increment_id(prefix, elt.children());
            }
        },
        decrement_id: function(prefix, elts){
            for (var i=0; i< elts.length; i++){
                var elt = $(elts[i]);
                ns.utils._increment_id(prefix, elt, ns.utils._attr, ATTRNAMES, -1);
                ns.utils._increment_id(prefix, elt, ns.utils._data, DATANAMES, -1);
                ns.utils.decrement_id(prefix, elt.children());
            }
        },
        _replace_id: function(prefix, elt, func, names, index){
            var re_id = new RegExp('^'+prefix+':(\\d+)');
            for (var key in names){
                var name = names[key];
                var value = func(elt, name);
                if(value){
                    var values = value.split(' ');
                    var output = [];
                    for(var i=0; i<values.length; i++){
                        var v = values[i];
                        var old_index = parseInt(v.replace(re_id, '$1'), 10);
                        var re = new RegExp('^'+prefix+':'+old_index);
                        var new_value = v.replace(re, prefix + ':' + index);
                        output.push(new_value);
                    }
                    func(elt, name, output.join(' '));
                }
            }
        },
        replace_id: function(prefix, elts, step, force_index){
            step = step || 1;
            var index = 0;
            for (var i=0; i< elts.length; i++){
                var elt = $(elts[i]);
                var tmp_index;
                if (typeof force_index !== 'undefined'){
                    tmp_index = force_index;
                }
                else{
                    tmp_index = index;
                }
                ns.utils._replace_id(prefix, elt, ns.utils._attr, ATTRNAMES, tmp_index);
                ns.utils._replace_id(prefix, elt, ns.utils._data, DATANAMES, tmp_index);
                ns.utils.replace_id(prefix, elt.children(), 1, tmp_index);

                // TODO: find why we need to have this step!
                // Perhaps by writing some tests!
                if (step === 1){
                    index += 1;
                }
                else if(((i+1) % step) === 0 && i !== 0){
                    index += 1;
                }
            }
        },
        truncate: function (str, limit) {
            var bits, i;
            bits = str.split('');
            if (bits.length > limit) {
                for (i = bits.length - 1; i > -1; --i) {
                    if (i > limit) {
                        bits.length = i;
                    }
                    else if (' ' === bits[i]) {
                        bits.length = i;
                        break;
                    }
                }
                bits.push('...');
            }
            return bits.join('');
        },
        get_first_class: function(obj){
            var cls = obj.attr('class');
            if (typeof cls === 'undefined') {
                return null;
            }
            return cls.split(' ')[0];
        }
    };

})(window.jQuery, xmltool);
