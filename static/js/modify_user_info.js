/**
 * This function is to modify user information
 * @param phone is user phone
 * @param introduction is user introduction
 * @param name is user name
 * @param password is user password
 * @param type is user type
 */
function modify_user_info(phone, introduction, name, password, type){
    $.ajax({
        url:type==="1"?"buyer/modifyBuyerInfo":"seller/modifySellerInfo",
        type:"post",
        dataType:"json",
        contentType: "application/json",
        data:JSON.stringify({
            phone:phone,
            introduction:introduction,
            name:name,
            password:password
        }),
        success: function (data){
            alert(data.message)

            // update base name
            $(".user-name").text(name)

            // reload
            render_user_info(type, phone)
        }
    })
}