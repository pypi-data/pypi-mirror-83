$(document).ready(function() {
    // check if we are in a edit card
    if ($("input[name=geocoding-address]").length === 0 &&
        $("input[id=form-widgets-subtitle]").length === 0 ) {return}
    $('li.formTab a').click(function(e){
        address = $('input#form-widgets-address').val();
        pc = $('input#form-widgets-zip_code').val();
        city = $('input#form-widgets-city').val();
        if ($('#form-widgets-ICoordinates-coordinates-wkt').val() == ""){
            complete_addr = address+" "+pc+" "+city;
            $("input[name=geocoding-address]").val(complete_addr);
        }
    });
});
