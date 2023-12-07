/**
 * This function is for user to delete account
 * @param phone is user phone to be deleted
 */
function delete_user(phone){
    if (!confirm("Delete?")){
        return;
    }

    $.ajax({
        url:"administer/deleteUser",
        type:"get",
        data:{phone: phone},
        success: function (data){
            alert(data.message)

            if (data.success){
                // clear session
                logout()
            }
        }
    })
}