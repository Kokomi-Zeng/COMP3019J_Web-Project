/**
 * This method is to render user info depend on the ajax response.
 * This method render data in user_info_box, user_amount_box
 * need type, phone
 */
function render_user_info(type, phone) {
    // console.log(type==="1")
    // console.log(type)
    $.ajax({
        url: type==="1"?"/buyer/buyerInfo":"/seller/sellerInfo",
        type: 'get',
        contentType: "application/json",
        dataType: "json",
        data:{
            phone: phone
        },
        success:function (data){
            // user
            $("#introduction").val(data.introduction)
            $("#name").val(data.name)

            // admin
            $("#introduction-span").text(data.introduction)
            $("#name-span").text(data.name)
            $("#status-span").text(data.status)
            $("#ban-user-button").text(data.status==='active'?"Ban User":"Unban User")
            status = data.status==='active'?"Ban User":"Unban User"
        }
    })
}
