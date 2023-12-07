/**
 *
 * @param DOM
 * @param product_id
 * @param phone
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