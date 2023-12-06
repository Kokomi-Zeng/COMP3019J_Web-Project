/**
 *
 * @param type
 * @param phone
 */
function reset_user_name(type, phone){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/user/resetUserName",
        type:"get",
        data:{phone:phone},
        success:function (data){
            console.log(data.message)
            render_user_info(type, phone)
        }
    })
}