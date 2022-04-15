$(document).ready(function(){

    //Contact form Handler
    // to show the form error under each form element
    // var contactForm = $('.contact-form2')

    // to show the form error on console.log
    var contactForm = $('.contact-form')
    var contactFormMethod = contactForm.attr('method')
    var contactFormEndPoint = contactForm.attr('action') 
    
    function displaySubmitting(submitBtn,defaultText, doSubmit){
        if (doSubmit){
        submitBtn.addClass('disabled')
        submitBtn.html('<i class="fa fa-spin fa-spinner"></i> Sending...')
        }else{
            submitBtn.removeClass('disabled')
            submitBtn.html(defaultText)
        }
        
    }
    contactForm.submit(function(event){
        var submitBtn = contactForm.find('[type="submit"]')
    var submitBtnTxt = submitBtn.text()
        event.preventDefault()
        var contactFormData= contactForm.serialize()
        var thisForm = $(this)

        displaySubmitting(submitBtn,"",true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndPoint,
            data: contactFormData,
            success:function(data){
                // thisForm[0].reset()
                contactForm[0].reset()
                // console.log('success for third')
                // console.log(data.message)

                setTimeout(function(){
                    displaySubmitting(submitBtn ,submitBtnTxt,false)
                },2000)
            },
            error: function(error){
                // console.log(error)
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ''
                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "<br />"
                    console.log(msg)
                })
                // $.alert({
                //     title: 'Oops!',
                //     content:msg,
                //     theme: "modern"
                // })
                setTimeout(function(){
                    displaySubmitting(submitBtn ,submitBtnTxt,false)
                },2000)
            }

        })
    })




    //Auto Search
    var  searchForm = $('.search-form')
    var searchInput = searchForm.find('[name="q"]')
    var typingTimer
    var typingInterval = 500 
    var searchBtn = searchForm.find('[type="submit"]')
    searchInput.keyup(function(event){
        // console.log(event)
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
    })

    function displaySearchingIcon(){
        searchBtn.addClass('disabled')
        searchBtn.html('<i class="fa fa-spin fa-spinner"></i> Searching...')
    }
    function performSearch(){
        displaySearchingIcon()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href  = '/search/?q=' + query
        },2000)
        
    }


    //Cart + add Products and add or remove cart form
       var ProductForm = $('.ajax-form-data')
       ProductForm.submit(function(event){
           event.preventDefault()
        //    console.log('Form is not sending')
           var thisForm = $(this)
           var actionEndPoint = thisForm.attr('action');
           actionEndPoint = thisForm.attr('data-endpoint');
           var httpMethod = thisForm.attr('method');
           var formData = thisForm.serialize();

        //    console.log('the data to be sent to ',actionEndPoint, ' with method ',httpMethod)

           $.ajax({

               url:actionEndPoint,
               method:httpMethod,
               data:formData,
               success: function(data){
                //    console.log('success')
                //This data with its attrs are coming from carts view show whether product added or removed
                //    console.log('Right data',data)
                //    console.log('Product added',data.added)
                //    console.log('Product removed', data.removed)
                   var submitSpan = thisForm.find('.submit-span')
                   //console.log(submitSpan.html())
                   // show an reaction after the user add or removes a cart 
                   if (data.added){
                       submitSpan.html('In cart <button class="btn btn-link">Remove?</button>')
                   }
                   else{
                       submitSpan.html('<button class="btn btn-success">Add to Cart</button>')
                   }
                    var navbarCounter = $('.navbar-cart-counter')
                   navbarCounter.text(data.navbarCartItemsCount)
                   //show location of cart and triggers an event if user is in cart
                   var currentPath = window.location.href
                   if (currentPath.indexOf('carts') != -1){
                       refreshCart()
                   }
                   
               },
               error:function(errorData){
                   console.log('error')
                   console.log(errorData)
               }
           })
       })
       // Refresh the carts page if the user removes a cart
       function refreshCart(){
        //    console.log('in cart currently')
           var cartTable = $('.cart-table')
           var cartBody = cartTable.find('.cart-body')
        //    cartBody.html('<h1>Changed</h1>')

           var productRows = cartBody.find('.cart-products')
           var currentUrl = window.location.href
           
           var refreshCartUrl= '/api/cart/'
           var refreshCartMethod = 'GET'
           var data  = {}
           $.ajax({
               url:refreshCartUrl,
               method:refreshCartMethod,
               data:data,
               success:function(data){
                //    console.log('Another success')
                //    console.log(data)

                var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
                   if (data.products.length > 0 ){
                    // productRows.html('<tr><td colspan=3>Coming Soon</td></tr>')
                    productRows.html(' ')
                    i=data.products.length
                    $.each(data.products,function(index,value){

                        // console.log(value)
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css('display','block')
                        // newCartItemRemove.removeClass('hidden-class')
                        newCartItemRemove.find('.cart-item-product-id').val(value.id)

                        cartBody.prepend("<tr><th scope=\'row\'>"+ i + "</th><td><a href='" +value.url +
                           "'>" + value.name + "</a>"+ newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i --
                    })
                    cartBody.find('.cart-total').text(data.total)
                    cartBody.find('.cart-tax-total').text(data.Tax_total)
                   }else{
                       window.location.href= currentUrl
                   }
               },
               error: function(errorData){
                console.log('error')
                console.log(errorData)
               }

           })
       }
   })