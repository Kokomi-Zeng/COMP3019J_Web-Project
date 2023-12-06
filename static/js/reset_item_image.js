
function reset_item_image(DOM, product_id){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/product/resetItemImage",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            get_item_image(DOM, product_id)
        }
    })
}