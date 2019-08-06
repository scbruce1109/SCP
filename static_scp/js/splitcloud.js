$(document).ready(function(){


/////////Auto Search Function
// Auto Search
var searchForm = $(".search-form")
var searchInput = searchForm.find("[name='q']") // input name='q'
var typingTimer;
var typingInterval = 500
var searchBtn = searchForm.find("[type='submit']")

searchInput.keyup(function(event){
  // key released
  clearTimeout(typingTimer)
  typingTimer = setTimeout(performSearch, typingInterval)

})

searchInput.keydown(function(event){
  // key pressed
  clearTimeout(typingTimer)

})

function displaySearching(){
  searchBtn.addClass('disabled')
  searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")

}

function performSearch(){
  displaySearching()
  var query = searchInput.val()
  setTimeout(function(){
    window.location.href='/search/?q=' + query
  }, 1000)

}


// Cart + Add Products
var productForm = $(".form-product-ajax")
console.log('durf')

// function getOwnedProduct(productId, submitSpan){
//   var actionEndpoint = '/orders/endpoint/verify/ownership'
//   var httpMethod = 'Get'
//   var data = {
//     product_id: productId
//   }
//   var isOwner
//   $.ajax({
//     url: actionEndpoint,
//     method: httpMethod,
//     data: data,
//     success: function(data){
//       console.log(data)
//       if (data.owner){
//         isOwner = true
//         submitSpan.html("<a class='btn btn-link' href='/library/'>In library</a>")
//       } else {
//         isOwner = false
//       }
//     },
//     error: function(){
//       console.log(error)
//     }
//   })
//   return isOwner
// }

// $.each(productForm, function(index, object){
//   var $this = $(this)
//   var isUser = $this.attr("data-user")
//   var submitSpan = $this.find(".submit-span")
//   var productInput = $this.find("[name='product_id']")
//   var productId = productInput.attr("value")
//   var productIsDigital = productInput.attr("data-is-digital")
//
//   if (productIsDigital && isUser){
//     var isOwned = getOwnedProduct(productId, submitSpan)
//   }
// })


productForm.submit(function(event){
  event.preventDefault();
  console.log("form is not sending");
  var thisForm = $(this);
  // var actionEndpoint = thisForm.attr("action");
  var actionEndpoint = thisForm.attr("data-endpoint")
  var httpMethod = thisForm.attr("method");
  var formData = thisForm.serialize();
  $.ajax({
    url: actionEndpoint,
    method: httpMethod,
    data: formData,
    success: function(data){
      var submitSpan = thisForm.find(".submit-span");
      if (data.added){
        submitSpan.html("<div class='btn-group'><a class='btn btn-link' href='/cart/'>In cart</a> <button type='submit' class='btn btn-link'>Remove?</button></div>")
      } else {
        submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
      }
      var navbarCount = $(".navbar-cart-count");
      var currentPath = window.location.href
      if (window.location.href.indexOf("cart") !=1) {
        refreshCart();
      }
      navbarCount.text("Cart " + data.cartItemCount)
    },
    error: function(errorData){
      $.alert({
        title: "Oh Heyyy",
        content: "an errorrrrr was happened"
      })
      console.log("error")
      console.log(errorData)
    }
  })
})

function refreshCart(){
  console.log("in current cart");
  var cartTable = $(".cart-table")
  var cartBody = cartTable.find(".cart-body")
  // cartBody.html("<h1>Changed</h1>")
  var productRows = cartBody.find(".cart-product")
  var currentUrl = window.location.href


  var refreshCartUrl = '/api/cart/';
  var refreshCartMethod = "GET";
  var data = {};
  $.ajax({
    url: refreshCartUrl,
    method: refreshCartMethod,
    data: data,
    success: function(data){

      var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
      if (data.products.length > 0){
        productRows.html(" ")
        i = data.products.length
        $.each(data.products, function(index, value){
          var newCartItemRemove = hiddenCartItemRemoveForm.clone()
          newCartItemRemove.css("display", "block")
          newCartItemRemove.find(".cart-item-product-id").val(value.id)
          cartBody.prepend("<tr><th scope=\"row\">" + i + "{{ forloop.counter }}</th><td colspan-3><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
          i--
        })

        cartBody.find(".cart-subtotal").text(data.subtotal)
        cartBody.find(".cart-total").text(data.total)
        console.log('heeeyyi')
      } else {
        console.log('ufff')
        window.location.href = currentUrl
      }
    },
    error: function(errorData){
      console.log("error")
      console.log(errorData)
    }
  })
}





})
