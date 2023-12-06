/**
 *
 * @param DOM
 * @param product_id
 */
function render_product_all_comment(DOM, product_id){
    $.ajax({
        url:"/comment/commentInfoById",
        type:"get",
        data:{
            product_id: product_id
        },
        success: function (data){
            render_comment(DOM, data)
        }
    })
}