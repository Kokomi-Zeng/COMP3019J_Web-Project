/**
 * This function is for admin to reset user image
 * @param DOM is JQuery Selector where the image is loaded
 * @param phone is user phone
 */
function reset_user_image(DOM, phone){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/user/resetUserImage",
        type:"get",
        data:{phone:phone},
        success:function (data){
            console.log(data.message)
            get_user_image(DOM, phone)
        }
    })
}