/**
 *
 * @param DOM
 * @param product_id
 */
function get_item_image(DOM, product_id){
    $.ajax({
        url: "/images/get_image_product",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data:{
            product_id: product_id,
        },
        success: function (data) {
            DOM.attr("src", data.url)
        }
    })
}