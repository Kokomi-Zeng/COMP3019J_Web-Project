/**
 * This function is to modify user information
 * @param phone is user phone
 * @param introduction is JQuery Selector where user introduction are
 * @param name is JQuery Selector where user name are
 * @param password JQuery Selector where is user password are
 * @param type JQuery Selector  whereis user type are
 */
function modify_user_info(phone, introduction, name, password, type){
    $.ajax({
        url:type==="1"?"buyer/modifyBuyerInfo":"seller/modifySellerInfo",
        type:"post",
        dataType:"json",
        contentType: "application/json",
        data:JSON.stringify({
            phone:phone,
            introduction:introduction.val(),
            name:name.val(),
            password:password.val()
        }),
        success: function (data){
            alert(data.message)

            // update base name
            $("#user-name").text(name.val())

            // reload
            render_user_info(type, phone)
        }
    })
}