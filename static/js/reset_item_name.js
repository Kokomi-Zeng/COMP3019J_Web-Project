
function reset_item_name(DOM, product_id){
    if (!confirm("Delete?")){
        return;
    }
    $.ajax({
        url:"/product/resetItemName",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            alert(data.message)
            render_item_info(product_id)
        }
    })
}