
function reset_item_name(DOM, product_id){
    if (!confirm("Reset?")){
        return;
    }
    $.ajax({
        url:"/products/resetItemName",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            render_item_info(product_id)
        }
    })
}