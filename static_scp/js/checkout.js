

function userFormToggle() {
  var loginBtn = document.getElementById('login-btn');
  var loginForm = document.getElementById('login-form');
  var guestRegisterForm = document.getElementById('guest-register-form');
  var guestRegisterBtn = document.getElementById('guest-register-btn');
  loginBtn.addEventListener('click', function() {
    loginForm.style.display = 'block';
    guestRegisterForm.style.display = 'none';
    console.log('login')
  })

  guestRegisterBtn.addEventListener('click', function() {
    guestRegisterForm.style.display = 'block';
    loginForm.style.display = 'none';
    console.log('guest')
  })
}

function userInfoToggle() {
  var infoEditBtn = document.getElementById('info-edit-btn');
  var infoForms = document.getElementById('info-forms');
  var infoDisplay = document.getElementById('info-display');

  infoEditBtn.addEventListener('click', function() {
    infoForms.style.display='block';
    infoDisplay.style.display = 'none';
  })
}


function billingAddressToggle() {
  var billingAddressEditBtn = document.getElementById('billing-address-edit-btn');
  var billingAddressForm = document.getElementById('billing-address-form');
  var billingAddressDisplay = document.getElementById('billing-address-display');
  var paymentEditBtn = document.getElementById('payment-edit-btn');
  var paymentForm = document.getElementById('payment-form');
  var paymentDisplay = document.getElementById('payment-display');

  billingAddressEditBtn.addEventListener('click', function() {
    billingAddressForm.style.display='block';
    billingAddressDisplay.style.display = 'none';
    paymentForm.style.display = 'none';
  })

  paymentEditBtn.addEventListener('click', function() {
    paymentForm.style.display='block';
    paymentDisplay.style.display = 'none';
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


window.addEventListener("load", () => {

  userFormToggle();
  userInfoToggle();
  billingAddressToggle();
  paymentMethodEdit();

})
