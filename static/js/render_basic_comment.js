function render_basic_comment(DOM, product_id){
    $.ajax({
        url:"/comment/commentBasicInfoById",
        type:"get",
        data:{
            product_id: product_id
        },
        success: function (data){
            render_comment(DOM, data)
        }
    })
}