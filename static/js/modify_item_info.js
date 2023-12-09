/**
 * This function is to modify item information
 * @param name is JQuery Selector where name is loaded
 * @param description is JQuery Selector where description is loaded
 * @param price is JQuery Selector where price is loaded
 * @param storage is JQuery Selector where storage is loaded
 * @param product_id is product id
 * @param phone is seller phone
 */
function modify_item_info(name, description, price, storage, product_id, phone){
    $.ajax({
        url:"products/modifyItem",
        type:"get",
        data:{
            seller_phone: phone,
            product_name: name.val(),
            description: description.val(),
            product_id: product_id,
            price: price.val(),
            storage: storage.val(),
        },
        success: function (data){
            alert(data.message)
            render_item_info(product_id)
        }
    })
}