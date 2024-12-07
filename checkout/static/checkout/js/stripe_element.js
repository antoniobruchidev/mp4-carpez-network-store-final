/*
    Core logic/payment flow for this comes from here:
    https://docs.stripe.com/payments/payment-element
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var bag = $('#bag').text()
var userId = $('#user_id').text();
const stripe = Stripe(stripePublicKey);
const appearance = { /* appearance */ };
const shipping = { mode: 'shipping' };
const payment = { mode: 'payment' };
const billing = { mode: 'billing' };
const elements = stripe.elements({ clientSecret, appearance });
const addressElement = elements.create('address', shipping);
const paymentElement = elements.create('payment', payment);
const billingElement = elements.create('address', billing);
addressElement.mount('#address-element');
paymentElement.mount('#payment-element');
billingElement.mount('#billing-element');


const form = document.getElementById('payment-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    $('.loading').removeClass('invisible')

    // From using {% csrf_token %} in the form
  
    var postData = {
      'csrfmiddlewaretoken': csrfToken,
      'client_secret': clientSecret,
      'email': $("#email").val(),
      'user_id': userId,
      'discount': discountId,
    };
    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(async function(e) {
        
        try {
            const data = await stripe.confirmPayment({
                //`Elements` instance that was used to create the Payment Element
                elements,
                redirect: 'if_required',
            });
            if (await data['paymentIntent']['status'] != 'succeeded') {
                // This point will only be reached if there is an immediate error when
                // confirming the payment. Show error to your customer (for example, payment
                // details incomplete)
                const messageContainer = document.querySelector('#error-message');
                messageContainer.textContent = data['paymentIntent']['error'].message;
            } else {
                // Your customer will be redirected to your `return_url`. For some payment
                // methods like iDEAL, your customer will be redirected to an intermediate
                // site first to authorize the payment, then redirected to the `return_url`.
                
                var details = {
                        "bag": JSON.parse(bag),
                        "stripe_pid": await data["paymentIntent"]["id"],
                        "shipping": JSON.stringify(await data["paymentIntent"]["shipping"]),
                        "email": $("#email").val(),
                        "discount": discountId,
                        }
                
                var json_details = JSON.stringify(details)

                const response = await fetch('/checkout/place_order/', {
                    headers: { 
                        "X-CSRFToken": csrfToken,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    method: 'POST',
                    body: json_details
                })
                const order_data = await response.json()
                window.location.href = `/checkout/checkout_success/${order_data['message']}` 
                
            }
            
        } catch (error) {
            console.log(error)
            $('.loading').addClass('invisible')
        }

    })

})