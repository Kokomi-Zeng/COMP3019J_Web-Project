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