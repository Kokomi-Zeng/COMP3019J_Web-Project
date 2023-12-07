/**
 * This function is to ban user depend on admin phone & user phone
 * @param admin_phone is admin phone
 * @param user_phone is user phone
 */
function ban_user(admin_phone, user_phone){
    $.ajax({
        url:"/administer/banUser",
        type:"get",
        data:{
            admin_phone:admin_phone,
            user_phone:user_phone
        },
        success:function (data){
            console.log(data.message)

            // reload user info
            render_user_info(type, phone)
        }
    })
}