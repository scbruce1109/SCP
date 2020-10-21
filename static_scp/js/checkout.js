
//////////mswitches between login and guest register form -- deactivated until we add user functionality
// function userFormToggle() {
//   var loginBtn = document.getElementById('login-btn');
//   var loginForm = document.getElementById('login-form');
//   var guestRegisterForm = document.getElementById('guest-register-form');
//   var guestRegisterBtn = document.getElementById('guest-register-btn');
//   loginBtn.addEventListener('click', function() {
//     loginForm.style.display = 'block';
//     guestRegisterForm.style.display = 'none';
//     console.log('login')
//   })
//
//   guestRegisterBtn.addEventListener('click', function() {
//     guestRegisterForm.style.display = 'block';
//     loginForm.style.display = 'none';
//     console.log('guest')
//   })
// }

function userInfoToggle() {
  var infoEditBtn = document.getElementById('info-edit-btn');
  var infoForms = document.getElementById('info-forms');
  var infoDisplay = document.getElementById('info-display');
  var billingAddressForm = document.getElementById('billing-address-form');
  var billingAddressDisplay = document.getElementById('billing-address-display');
  var paymentForms = document.getElementById('payment-forms');
  var paymentMethods = document.getElementById('payment-methodss');

  if (infoEditBtn) {
    infoEditBtn.addEventListener('click', function() {
      infoForms.style.display='table';
      infoDisplay.style.display = 'none';
      billingAddressForm.style.display = 'none';
      billingAddressDisplay.style.display = 'none';
      paymentForms.style.display = 'none';
      paymentMethods.style.display = 'none';
    })
  }
}


function billingAddressToggle() {
  var billingAddressEditBtn = document.getElementById('billing-address-edit-btn');
  var billingAddressForm = document.getElementById('billing-address-form');
  var billingAddressDisplay = document.getElementById('billing-address-display');
  var paymentEditBtn = document.getElementById('payment-edit-btn');
  var paymentForm = document.getElementById('payment-form');
  var paymentDisplay = document.getElementById('payment-display');

  if (billingAddressEditBtn) {
    billingAddressEditBtn.addEventListener('click', function() {
      billingAddressForm.style.display='block';
      billingAddressDisplay.style.display = 'none';
      paymentForm.style.display = 'none';
    })
}

  if (paymentEditBtn) {
    paymentEditBtn.addEventListener('click', function() {
      paymentForm.style.display='block';
      paymentDisplay.style.display = 'none';
    })
}

}

function paymentMethodSwitch() {
  var creditCardBtn = document.getElementById('credit-card-btn');
  var paypalBtn = document.getElementById('paypal-btn');
  var creditCardCont = document.getElementById('stripe-container');
  var paypalCont = document.getElementById('paypal-container');

  creditCardBtn.addEventListener('click', function() {
    creditCardCont.style.display='block';
    paypalCont.style.display = 'none';
    creditCardBtn.className += ' active-txt';
    paypalBtn.classList.remove('active-txt');
  })

  paypalBtn.addEventListener('click', function() {
    creditCardCont.style.display='none';
    paypalCont.style.display = 'block';
    paypalBtn.className += ' active-txt';
    creditCardBtn.classList.remove('active-txt');
  })

}

// function paymentMethodEdit() {
//   var paymentEditBtn = document.getElementById('payment-edit-btn');
//   var paymentForm = document.getElementById('payment-form');
//   var paymentDisplay = document.getElementById('payment-display');
//
//   paymentEditBtn.addEventListener('click', function() {
//     paymentForm.style.display='block';
//     paymentDisplay.style.display = 'none';
//   })
// }



function discountCodeApply() {
  var discountForm = $("#discount-form")
  console.log(discountForm)
  $("#discount-form").submit(function(e){
    e.preventDefault();
    var thisForm = $(this);
    // var actionEndpoint = thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint")
    console.log(actionEndpoint);
    var discountValue = $('#discount-input').val()
    console.log(discountValue);
    $.ajax({
        url : actionEndpoint, // the endpoint
        type : "POST", // http method
        data : { discount_code : $('#discount-input').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#discount-input').val(''); // remove the value from the input
            if (json['success']) {
              $('#cart-total').html('<b>$' + json['new_total']+'</b>');
              $('#cart-total-hidden').attr('total', json['new_total'])
              $('#discount-form-messages').html(json['message'])
              $('#discount-amount').html('- $' + json['discount_amount']);
              $('#discount-form-container').attr('style', 'display:none;')
            }
            else {
              $('#discount-form-messages').html(json['message'])
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
})
}


window.addEventListener("load", () => {

  // userFormToggle();
  userInfoToggle();
  billingAddressToggle();
  paymentMethodSwitch();
  discountCodeApply();




})
