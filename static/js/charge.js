/**
 * This function will update user charge amount
 * @param current_money_DOM
 * @param charge_num_DOM
 * @param phone
 */
function charge(current_money_DOM, charge_num_DOM, phone){
    $.ajax({
        url:'/buyer/charge',
        type:'get',
        data:{
            phone:phone,
            charge_num: charge_num_DOM.val(),
        },
        success:function (data){
            alert(data.message)
            if (data.success){
                charge_num_DOM.empty();
                render_money(current_money_DOM, phone)
            }
        }
    })
}