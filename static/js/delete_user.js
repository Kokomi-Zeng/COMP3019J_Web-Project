
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
            logout()
        }
    })
}