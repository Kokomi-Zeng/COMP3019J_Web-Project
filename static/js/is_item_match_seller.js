function is_item_match_seller(product_id){
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