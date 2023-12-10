/**
 * This function is for admin to reset product name
 * @param product_id is product id
 */
function reset_item_name(product_id){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/products/resetItemName",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            // reload
            render_item_info(product_id)
        }
    })
}