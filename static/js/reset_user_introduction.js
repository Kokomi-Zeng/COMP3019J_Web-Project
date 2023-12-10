/**
 * This function is for admin to reset user introduction
 * @param type is user type
 * @param phone is user phone
 */
function reset_user_introduction(type, phone){
    console.log(type)
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/user/resetUserIntroduction",
        type:"get",
        data:{phone:phone},
        success:function (data){
            console.log(data.message)
            render_user_info(type, phone)
        }
    })
}