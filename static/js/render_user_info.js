/**
 * This method is to render user info depend on the ajax response.
 * This method render data in user_info_box, user_amount_box
 * need type, phone
 */
function render_user_info(type, phone) {
    $.ajax({
        url: type==="1"?"/buyer/buyerInfo":"/seller/sellerInfo",
        type: 'get',
        contentType: "application/json",
        dataType: "json",
        data:{
            phone: phone
        },
        success:function (data){
            $("#introduction").val(data.introduction)
            $("#name").val(data.name)
            $("#phone").innerText = phone;
        }
    })
}
