$(document).ready(function () {
    monkeyPatchAutocomplete();

    $("#input1").autocomplete({
        // The source option can be an array of terms.  In this case, if
        // the typed characters appear in any position in a term, then the
        // term is included in the autocomplete list.
        // The source option can also be a function that performs the search,
        // and calls a response function with the matched entries.
        source: "generate",
        minLength: 5,

        select: function (value, data) {
            var s = ""
            if (typeof data == "undefined") {
                s = value;
            } else {
                s = data.item.value;
            }
            if (s.length > 30) { s = s.substring(0, 30) + "..."; }
            addMessage('You selected: ' + s + "<br/>");
        }
    });
});

// This patches the autocomplete render so that
// matching items have the match portion highlighted.
function monkeyPatchAutocomplete() {

    // Don't really need to save the old fn,
    // but I could chain if I wanted to
    var oldFn = $.ui.autocomplete.prototype._renderItem;

    $.ui.autocomplete.prototype._renderItem = function (ul, item) {
        var re = new RegExp("\\b" + this.term, "i");
        var t = item.label.replace(re, "<span style='font-weight:bold;color:Blue;'>" + this.term + "</span>");
        return $("<li></li>")
            .data("item.autocomplete", item)
            .append("<a>" + t + "</a>")
            .appendTo(ul);
    };
}

function addMessage(msg) {
    $('#msgs').append(msg + "<br/>");
}