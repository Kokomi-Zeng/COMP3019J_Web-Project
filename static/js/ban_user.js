
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
            render_user_info(type, phone)
        }
    })
}