/**
 * This method is to upload user image
 * @param DOM
 * @param form_data contains image
 * @param phone
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