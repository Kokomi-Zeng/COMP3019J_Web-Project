/**
 * This method is for user to upload user image
 * @param DOM is JQuery Selector where the image is loaded
 * @param form_data is Formdata object that contains image
 * @param phone is user phone
 */
function upload_user_image(DOM, form_data, phone){
    $.ajax({
        url:"/images/upload_image_user?phone=" + phone,
        type:"post",
        data:form_data,
        dataType:"json",
        processData:false,
        contentType:false,
        success:function (data){
            console.log(data.message)
            get_user_image(DOM, phone)
        }
    })
}