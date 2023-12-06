/**
 * this method is for $("img") to set their src.
 * @param DOM is the img that need to set src.
 * @param phone
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