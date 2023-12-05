function modify_user_info(){
    $.ajax({
        url:type==="1"?"buyer/modifyBuyerInfo":"seller/modifySellerInfo",
        type:"get",
        data:{
            phone:phone,
            introduction: $("#introduction").val(),
            name:$("#name").val(),
            password:$("#password").val()
        },
        success: function (data){
            console.log(data.message)
        }
    })
}