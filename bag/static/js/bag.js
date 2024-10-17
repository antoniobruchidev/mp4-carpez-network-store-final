// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`#quantity-${itemId}`).val());
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
    console.log("something")
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
$('.update-product').click(function(e) {
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    var itemId = $(this).attr('id').split('update-')[1];
    var quantity = $(`#quantity-${itemId}`).val();
    var data = {'csrfmiddlewaretoken': csrfToken, 'quantity': quantity}
    var url = `update/${itemId}`;
    
    $.post(url, data)
     .done(function() {
        location.reload();
     })
    
})

// Remove item and reload on click
$('.remove-product').click(function(e) {
    itemId = $(this).attr('id').split('remove-')[1]
    url = `remove/${itemId}`
    window.location.href = url
})