/**
 * This function is for seller to delete item
 * @param product_id is product id to be deleted
 * @param phone is seller phone
 */
function delete_item(product_id, phone){
    if (!confirm("Delete?")){
        return;
    }
    $.ajax({
        url:"/products/deleteItem",
        type:"get",
        data:{
            product_id: product_id,
            seller_phone: phone
        },
        success: function (data){
            alert(data.message)

            if (data.success){
                // Jump to shop page
                window.location.replace("/shop")
            }
        }
    })
}