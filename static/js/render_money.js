/**
 * This function is to render buyer money
 * @param DOM is JQuery Selector where buyer money is loaded
 * @param phone is buyer phone
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
                // Insert Data
                DOM.text("Current Money: " + data.money);
            }else {
                console.log(data.message)
            }
        }
    })
}