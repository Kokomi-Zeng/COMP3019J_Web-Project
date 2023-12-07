/**
 * This method is to render all comments of a product
 * @param DOM is JQuery Selector where comments are loaded
 * @param product_id is product id
 * @param phone is user phone
 */
function render_product_all_comment(DOM, product_id, phone){
    $.ajax({
        url:"/comment/commentInfoById",
        type:"get",
        data:{
            product_id: product_id,
            phone: phone
        },
        success: function (data){
            render_comment(DOM, data)
        }
    })
}