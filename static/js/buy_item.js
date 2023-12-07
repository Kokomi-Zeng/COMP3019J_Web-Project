/**
 * This function is for buyer to buy product
 * @param buy_num_DOM is jQuery selector object
 * @param product_id is product id
 * @param phone is user phone
 */
function buy_item(buy_num_DOM, product_id, phone){
    $.ajax({
        url: "/buyer/buyItem",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data: {
            product_id: product_id,
            phone: phone,
            quantity: buy_num_DOM.val(),
        },
        success: function (data) {
            alert(data.message);
            if (data.success) {
                buy_num_DOM.val("")
                render_item_info(product_id)
            }
        }
    })
}