/**
 * This function is for admin to reset item image
 * @param DOM is JQuery Selector where the image is loaded
 * @param product_id is product id
 */
function reset_item_image(DOM, product_id){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/products/resetItemImage",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            get_item_image(DOM, product_id)
        }
    })
}