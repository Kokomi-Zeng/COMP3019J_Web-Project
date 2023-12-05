/**
 * This function will update user charge amount
 * @param form_data contains
 * phone
 * charge_num
 */
function charge(form_data){
    $.ajax({
        url:'/buyer/charge',
        type:'get',
        data:{
            phone: form_data.get("phone"),
            charge_num: form_data.get("charge_num"),
        },
        success:function (data){
            alert(data.message)

        }
    })
}