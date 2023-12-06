function delete_item(product_id, phone){
    if (!confirm("Delete?")){
        return;
    }
    $.ajax({
        url:"/products/deleteItem",
        type:"get",
        data:{
            product_id: product_id,
            seller_phone: phone
        },
        success: function (data){
            alert(data.message)
            window.location.replace("/shop")
        }
    })
}