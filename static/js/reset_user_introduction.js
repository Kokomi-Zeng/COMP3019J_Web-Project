
function reset_user_introduction(type, phone){
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