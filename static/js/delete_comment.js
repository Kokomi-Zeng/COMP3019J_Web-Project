
function delete_comment(DOM, comment_id){
    $.ajax({
        url:"/administer/deleteComment",
        type:"get",
        data:{
            comment_id: comment_id
        },
        success: function (data){
            alert(data.message)
            render_all_comment(DOM)
        }
    })
}