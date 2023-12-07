/**
 * This method is to load user image
 * @param DOM is JQuery selector where user image is loaded
 * @param phone is user phone
 */
function get_user_image(DOM, phone){
    $.ajax({
        url: "/images/get_image_user",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data:{
            phone: phone,
        },
        success: function (data) {
            DOM.attr("src", data.url)
        }
    })
}