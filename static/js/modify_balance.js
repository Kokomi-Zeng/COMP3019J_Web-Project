/**
 *
 * @param phone
 * @param amount
 */
function modify_balance(phone, amount){
    if (!confirm("Delete?")){
        return;
    }
    $.ajax({
        url:"/administer/updateBuyerAccount",
        type:"get",
        data:{
            phone: phone,
            amount: amount,
        },
        success: function (data){
            alert(data.message)
            render_user_info("1", phone)
        }
    })
}