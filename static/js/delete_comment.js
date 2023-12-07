/**
 * This function is for admin to delete comment
 * @param DOM is where comment are rendered
 * @param comment_id deleted comment id
 */
function delete_comment(DOM, comment_id){
    if (!confirm("Delete?")){
        return;
    }
    $.ajax({
        url:"/administer/deleteComment",
        type:"get",
        data:{
            comment_id: comment_id
        },
        success: function (data){
            alert(data.message)
            // reload
            render_all_comment(DOM)
        }
    })
}