function logout(){
    $.ajax({
        url:"/clearSession",
        type:"get",
        success:function (data){
            if (data.success){
                window.location.replace("/shop")
            }else {
                console.log(data.message)
            }
        }
    })
}