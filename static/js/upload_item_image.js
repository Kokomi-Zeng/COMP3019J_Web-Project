/**
 * This function is to upload image depend on fromdata and product id
 * @param formdata is FormData object that contains product image
 * @param product_id is product id
 * @param DOM
 */
function upload_item_img(DOM, formdata, product_id){
    $.ajax({
        url:"/images/upload_image_product?product_id=" + product_id,
        type:"post",
        data:formdata,
        dataType:"json",
        processData:false,
        contentType:false,
        success:function (data){
            alert(data.message);
            if (data.success) {
                get_item_image(DOM, product_id)
            }
        }
    })
}