// Javascript-Code für Projektevaluation

$(document).ready(function() {
    var config = {
        '.chosen-select'           : {},
        /* noch nicht verwendet: */
        '.chosen-select-deselect'  : {allow_single_deselect:true},
        '.chosen-select-no-single' : {disable_search_threshold:10},
        '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'},
        '.chosen-select-width'     : {width:"95%"}
    }
    for (var selector in config) {
        $(selector).chosen(config[selector]);
    }

    function counting_matters() {
        //get the limit from maxlength attribute
        var limit = parseInt($(this).data('maxlength'), 10);
        //get the current text inside the textarea
        var text = $(this).val();
        //count the number of characters in the text
        var chars = text.length;

        //check if there are more characters then allowed
        if (chars > limit) {
            var tolerance = $(this).data('tolerance');
            if (typeof tolerance !== "undefined") {
                uselimit = limit + parseInt(tolerance, 10);
            } else {
                uselimit = limit;
            }
            if (chars > uselimit) {
                //and if there are use substr to get the text before the limit
                // text = typeof tolerance + ' ' + tolerance + ' ' + text;
                var new_text = text.substr(0, uselimit);

                //and change the current text with the new text
                $(this).val(new_text);
            }
        }
        // Für Anzeige weiterhin das Limit ohne Toleranzzugabe:
        var left = chars > limit ? 0 : limit - chars;
        var counter_selector = $(this).data('counter');
        if (counter_selector) {
            $(counter_selector).html(left);
        }
    }
    $('textarea.limited-length').keyup(counting_matters);
    $('textarea.limited-length').change(counting_matters);

    $('textarea, input.text').keypad({
        keypadOnly: false,
        // Anordnung wie auf dem Telefon;
        // erst Super-, dann Subscript:
        // vim: s,\(\\u[02][0-9ab]\{3\}\)\(\\u[02][0-9ab]\{3\}\)\(\\u[02][0-9ab]\{3\}\)\(\\u[02][0-9ab]\{3\}\)\(\\u[02][0-9ab]\{3\}\)\(\\u[02][0-9ab]\{3\}\),\2\4\6\1\3\5,
        'prompt': 'Sonderzeichen einfügen',
        layout: ['\u2081\u2082\u2083'+$.keypad.HALF_SPACE+'\u00b9\u00b2\u00b3', // + $.keypad.CLOSE,
                 '\u2084\u2085\u2086'+$.keypad.HALF_SPACE+'\u2074\u2075\u2076',
                 '\u2087\u2088\u2089'+$.keypad.HALF_SPACE+'\u2077\u2078\u2079',
                 '\u208b\u2080\u208a'+$.keypad.HALF_SPACE+'\u207b\u2070\u207a'],
        showOn: 'focus' // oder 'button'
    });

    $('.datatb-12').dataTable({
        sDom: "<'row'<'col-md-7'i><'col-md-5 text-right pull-right'f>><'row'<'col-md-3'l>r<'col-md-9 text-right pull-right'p>>t<<'col-md-12 pull-right text-right'p>>",

        // "sPaginationType": "bootstrap", // (not used because of styles bug)
        oLanguage: {
            sUrl: '@@collective.js.datatables.translation'
        }
        });
    $('input,select,textarea').each(function () {
        var elem = $(this);
        if (elem.prop('readonly')) return;
        if (!elem.attr('name')) {
            elem.attr('style', 'border: 2px dashed red; padding: 2px');
            var theid = elem.attr('id'),
                thetype = elem.attr('type');
            if (theid) {
                elem.attr('name', theid);
            }
            if (thetype === 'hidden') {
                elem.attr('type', 'text');
            }
        }
    });
});

// vim: ts=4 sts=4 sw=4 noet
