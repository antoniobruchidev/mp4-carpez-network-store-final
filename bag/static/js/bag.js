// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`#item-${itemId}`).val());
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;
    $(`#decrement-${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-${itemId}`).prop('disabled', plusDisabled);
    console.log()
}

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty-input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('id');
    handleEnableDisable(itemId);
}

// Check enable/disable every time the input is changed
$('.qty-input').on('change', function() {
    var itemId = $(this).data('id');
    handleEnableDisable(itemId);
});

// Increment quantity
$('.add-1').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).prev('div').children()[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).focus()
    $(closestInput).val(currentValue + 1);
    var itemId = $(this).data('id');
    //handleEnableDisable(itemId);
    console.log("INCREMENTED", closestInput)
    $(closestInput).trigger('change', handleEnableDisable(itemId))
})

// Decrement quantity
$('.remove-1').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).next('div').children()[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue - 1);
    $(this).focus()
    var itemId = $(this).data('id');
    //handleEnableDisable(itemId);
    console.log("DECREMENTED", closestInput)
    $(closestInput).trigger('change', handleEnableDisable(itemId))
})

// Update quantity on click
$('.update').click(function(e) {
    var form = $(this).prev('.update-form');
    form.submit();
})

// Remove item and reload on click
$('.remove-product').click(function(e) {
    var csrfToken = "{{ csrf_token }}";
    var itemId = $(this).attr('id').split('remove_')[1];
    var url = `remove/${itemId}/`;
    var data = {'csrfmiddlewaretoken': csrfToken};

    $.post(url, data)
     .done(function() {
         location.reload();
     });
})