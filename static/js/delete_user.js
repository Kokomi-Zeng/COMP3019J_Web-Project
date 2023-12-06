
function delete_user(phone){
    $.ajax({
        url:"administer/",
        type:"get",
        data:{phone: phone},
        success: function (data){
            alert(data.message)
            window.location.replace("/shop")
        }
    })
}