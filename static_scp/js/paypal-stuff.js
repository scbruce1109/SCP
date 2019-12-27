function paypalOrderHandler(orderID) {
  var orderIdEndpoint = '/cart/paypal-transaction-complete/'
  var post_data = {
    'order_id': orderID
  }
  $.ajax({
    data: post_data,
    url: orderIdEndpoint,
    method: "POST",
    success: function(data){
      console.log("payapl thing successful")
      console.log(orderID)
      window.location.href='/cart/checkout/success'

    },
    error: function(error){
      console.log(error)
    }
  })
}

var cart_total = document.getElementById('cart-total-hidden')
var total = cart_total.getAttribute('total')

paypal.Buttons({
  style: {
    layout: 'horizontal',
   fundingicons: 'false',
   tagline: 'false',
    },
    funding: {
      disallowed: [ paypal.FUNDING.CREDIT ]
    },

  createOrder: function(data, actions) {


    // Set up the transaction
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: total
        }
      }]
    });
  },
  onApprove: function(data, actions) {
    // Capture the funds from the transaction
    return actions.order.capture().then(function(details) {
      // Show a success message to your buyer
      alert('Transaction completed by ' + details.payer.name.given_name);
      // Call your server to save the transaction
      paypalOrderHandler(data.orderID)
    });
  }
}).render('#paypal-button-container');
