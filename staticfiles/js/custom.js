//jqdoc (快捷鍵)
$(document).ready(function () {
    //jqclick (快捷鍵)
    $('.increment-btn').click(function (e){
        e.preventDefault();
                        //jqfind (快捷鍵)
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10)
        value = isNaN(value) ? 0: value;
        if(value < 10) {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    })

    $('.decrement-btn').click(function (e){
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value,10)
        value = isNaN(value) ? 0: value;
        if(value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    })

    $('.cart-increment-btn').click(function (e){
        e.preventDefault();
                        //jqfind (快捷鍵)
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10)
        value = isNaN(value) ? 0: value;
        if(value < 10) {
            value++;
            $('.qty-input').val(value);
        }
    });

    $('.cart-decrement-btn').click(function (e){
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value,10)
        value = isNaN(value) ? 0: value;
        if(value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
    
    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
                    //jqval (快捷鍵)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        //jqajax (快捷鍵)
        $.ajax({
            method: "POST",
            url: "/add_to_cart",    //如果前面不加 / url會直接接在當前的url後面
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken:token
            },
            //dataType: "dataType",   這行若不刪掉，下面success的response會出不來
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                $('#navbarNav').load(location.href + " #navbarNav");
            }
        }); 
    });

    $(document).on('click','.addToWishlist', function (e) {
        e.preventDefault();
        
        var product_id = $(this).data('id');
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/add_to_wishlist",    
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
                $('#navbarNav').load(location.href + " #navbarNav");
                
                //swal("Good job!", "You clicked the button!", "success").then((value) => {
                    //window.location.herf = '/home'   //可以再按完按鈕之後指定要去的url
                  //});
            }
        }); 
    });

    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/update_cart",    
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                console.log(response)
                location.reload()
                //alertify.success(response.status)
            }
        }); 
    });

    //jqon (快捷鍵)
    $(document).on('click','.delete-cart-item', function (e) {  //用這個會整個網頁 reload
  //$('.delete-cart-item').click(function (e) {  //如果用這行只會reload<div class="delete-cart-item"></div>
        e.preventDefault();                      //裡面的東西而已，外面的都不會reload
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete_cart_item",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                //jqload (快捷鍵)                    //.cart_data前面要空一個不然會報錯
                $('.cart_data').load(location.href + " .cart_data");  //reload '.cart_data' 裡面的東西
                $('#navbarNav').load(location.href + " #navbarNav");
            }
        });
    });
    
    $(document).on('click','.delete-wishlist-item', function (e) {
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete_wishlist_item",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                //https://blog.csdn.net/LIU_YANZHAO/article/details/79589547 局部reload
                $('.wish_data').load(location.href + " .wish_data");    
                $('#navbarNav').load(location.href + " #navbarNav");
            }
        });
    });

    $(document).on('click','.activateBtn', function () {
        let card_id = $(this).attr('data-id');
        $.ajax({
            url: "/acticate_address",
            data: {
                'id' : card_id
            },
            dataType: "json",
            success: function (res) {
                if(res.bool == true) {
                    $('.addicon').hide();
                    $('.addicon' + card_id).show();

                    $('.activateBtn').show();
                    $('.activateBtn' + card_id).hide();

                    $('.addcard').removeClass('shadow border-danger');
                    $('.addcard' + card_id).addClass('shadow border-danger');

                }
            }
        });
    });

    $(document).on('click','.addEdit', function () {
        let card_id = $(this).attr('data-id');
        
        $.ajax({
            url: "/edit_address",
            data: {
                'id' : card_id
            },
            dataType: "json",
            success: function (res) {
                $('.form-content').html(res.data);
            }
        });
    });

    $('.addForm').submit(function (e) { 
        console.log($(this).serialize())
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (res) {
                if(res.bool == true) {
                    $('.modal').modal('hide');
                    location.reload()
                    //$('.addContent').load(location.href + ' .addContent');
                }
            }
        });
        e.preventDefault();
        
    });
    
});

