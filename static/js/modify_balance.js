/**
 * This function is for admin to modify user account
 * @param DOM is JQuery Selector where current money is in
 * @param amount is modify amount
 * @param phone is user phone
 */
function modify_balance(DOM, amount, phone){
    if (!confirm("Modify?")){
        return;
    }
    $.ajax({
        url:"/administer/updateBuyerAccount",
        type:"get",
        data:{
            phone: phone,
            amount: amount.val(),
        },
        success: function (data){
            alert(data.message)
            render_money(DOM, phone)
        }
    })
}