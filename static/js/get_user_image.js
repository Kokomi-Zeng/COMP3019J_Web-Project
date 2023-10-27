/**
 * this method is for $("img") to set their src.
 * @param img is the img that need to set src.
 */
function get_user_image(img){
    $.ajax({
        url: "/images/get_image_user",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data:{
            phone: phone,
        },
        success: function (data) {
            img.attr("src", data.url)
        }
    })
}