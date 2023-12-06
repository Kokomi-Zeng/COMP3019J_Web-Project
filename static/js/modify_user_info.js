/**
 * This function is to modify user information
 * @param form_data contains
 * phone
 * introduction
 * name
 * password
 */
function modify_user_info(form_data){
    $.ajax({
        url:type==="1"?"buyer/modifyBuyerInfo":"seller/modifySellerInfo",
        type:"post",
        dataType:"json",
        contentType: "application/json",
        data:JSON.stringify({
            phone:form_data.get("phone"),
            introduction:form_data.get("introduction"),
            name:form_data.get("name"),
            password:form_data.get("password")
        }),
        success: function (data){
            alert(data.message)
            render_user_info(type, form_data.get("phone"))
        }
    })
}