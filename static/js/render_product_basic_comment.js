/**
 * This function si to render basic comments of a product
 * Only render Top 5 and Low 5 comments
 * @param DOM is JQuery Selector where comments are loaded
 * @param product_id is product id
 */
function render_product_basic_comment(DOM, product_id){
    $.ajax({
        url:"/comment/commentBasicInfoById",
        type:"get",
        data:{
            product_id: product_id
        },
        success: function (data){
            render_comment(DOM, data)
        }
    })
}