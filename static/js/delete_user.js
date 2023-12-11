/**
 * This function is for user to delete account
 * @param phone is user phone to be deleted
 * @param isAdmin is authority
 */
function delete_user(phone, isAdmin){
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
                if (isAdmin){
                    // back to admin page
                    window.location.href = "/admin"
                }else {
                    // clear session
                    logout()
                }
            }
        }
    })
}