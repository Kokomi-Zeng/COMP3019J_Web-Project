/**
 * This function is to modify item info
 * @param name INPUT
 * @param description INPUT
 * @param price INPUT
 * @param storage INPUT
 * @param product_id is product_id
 * @param phone is phone
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
        }
    })
}