// Disable +/- buttons outside 1-99 range
function handleEnableDisable() {
    var currentValue = parseInt($(`#rating`).val());
    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 4;
    $(`#decrement-rating`).prop('disabled', minusDisabled);
    $(`#increment-rating`).prop('disabled', plusDisabled);
    console.log()
}

// Ensure proper enabling/disabling of all inputs on page load
handleEnableDisable();


// Check enable/disable every time the input is changed
$('.qty-input').on('change', handleEnableDisable);

// Increment quantity
$('.add-1').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).prev('div').children()[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).focus()
    $(closestInput).val(currentValue + 1);
    var itemId = $(this).data('id');
    $(closestInput).trigger('change', handleEnableDisable)
})

// Decrement quantity
$('.remove-1').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).next('div').children()[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue - 1);
    $(this).focus()
    var itemId = $(this).data('id');
    $(closestInput).trigger('change', handleEnableDisable)
})