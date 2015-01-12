$(document).ready(function() { 
    // Setup select2 widget on language selection and choose English as default
    $(".select2-lang").select2(); 
    if ($(".select2-lang").select2("val").length == 0) {
        $(".select2-lang").select2("val", "1");
    }

    $(".select2-lang").on('add_select', function(event, new_id) {
        var val = $(".select2-lang").select2("val");
        $(".select2-lang").select2("val", val);
    });

});