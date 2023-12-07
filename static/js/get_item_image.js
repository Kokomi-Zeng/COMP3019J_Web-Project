/**
 * This function is to load product image
 * @param DOM is JQuery selector where picture is loaded
 * @param product_id is product id
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
            // load image
            DOM.attr("src", data.url)
        }
    })
}