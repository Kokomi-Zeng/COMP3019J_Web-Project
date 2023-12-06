function delete_item(product_id){
    $.ajax({
        url:"/products/deleteItem",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            window.location.replace("/shop")
        }
    })
}