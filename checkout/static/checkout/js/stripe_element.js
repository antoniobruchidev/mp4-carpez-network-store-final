/*
    Core logic/payment flow for this comes from here:
    https://docs.stripe.com/payments/payment-element
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);
const appearance = { /* appearance */ };
const options = { mode: 'shipping'};
const optionsB = { mode: 'billing'};
const elements = stripe.elements({ clientSecret, appearance });
const addressElement = elements.create('address', options);
const paymentElement = elements.create('payment', optionsB);
addressElement.mount('#address-element');
paymentElement.mount('#payment-element');

