/**
 * this method is to justify whether the product is belongs to the certain suer.
 * belong = true when user is its owner.
 * belong = false otherwise.
 * need param product_id
 */
function is_item_match_seller(){
    $.ajax({
        url:"/shop/isItemMatchSeller",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data:{
            product_id: product_id,
            phone: phone
        },
        success:function (data){
            belong = data.belong;
            $(document).trigger("belongLoaded");
        }
    })
}