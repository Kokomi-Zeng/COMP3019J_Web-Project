/**
 * This function is to render buyer money
 * @param DOM
 * @param phone is user phone
 */
function render_money(DOM, phone){
    $.ajax({
        url: "/buyer/getMoney",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data: {
            phone: phone,
        },
        success: function (data) {
            if (data.success){
                DOM.text("Current Money: " + data.money);
            }else {
                console.log(data.message)
            }
        }
    })
}