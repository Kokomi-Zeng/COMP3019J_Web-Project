/**
 * This function is for seller to upload product image
 * @param DOM is JQuery Selector where the image is loaded
 * @param formdata is FormData object that contains product image
 * @param product_id is product id
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