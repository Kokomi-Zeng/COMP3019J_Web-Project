/**
 *
 * @param DOM
 */
function render_all_comment(DOM){
    $.ajax({
        url:"/comment/getAllComments",
        type:"get",
        success: function (data){
            render_data(DOM, data)
        }
    })
}

function render_data(DOM, data){
    DOM.empty();

    for (let i=0; i<data.length; i++){
        const comment = data[i]

        // Render DIV comment box
        const comment_box = document.createElement("div")
        comment_box.setAttribute("class", "comment-box");
        DOM.append(comment_box)

        // Render IMG commenter image
        const commenter_img_div = document.createElement("div")
        const commenter_img = document.createElement("img")
        commenter_img_div.setAttribute("class", "commenter-img-box")
        commenter_img.setAttribute("class" ,"commenter-img")
        commenter_img.setAttribute("src", comment.user_image)
        comment_box.append(commenter_img_div)
        commenter_img_div.append(commenter_img)

        // Render DIV comment info
        const comment_info_div = document.createElement("div")
        comment_info_div.setAttribute("class", "comment-info-box")
        comment_box.append(comment_info_div)

        // Render SPAN comment id
        const comment_id_div = document.createElement("div")
        const comment_id = document.createElement("span")
        comment_id_div.setAttribute("class", "comment-id-box")
        comment_id.setAttribute("class" ,"comment-id")
        comment_id.innerText = "Comment Id: " + comment.comment_id
        comment_info_div.append(comment_id_div)
        comment_id_div.append(comment_id)

        // Render SPAN commenter name
        const commenter_name_div = document.createElement("div")
        const commenter_name = document.createElement("span")
        commenter_name_div.setAttribute("class", "commenter-name-box")
        commenter_name.setAttribute("class" ,"commenter-name")
        commenter_name.innerText = "Commenter: " + comment.commenter_name
        comment_info_div.append(commenter_name_div)
        commenter_name_div.append(commenter_name)

        // Render SPAN rating
        const comment_rating_div = document.createElement("div")
        const comment_rating = document.createElement("span")
        comment_rating_div.setAttribute("class", "comment-rating-box")
        comment_rating.setAttribute("class" ,"comment-rating")
        comment_rating.innerText = "Rating: " + comment.rating
        comment_info_div.append(comment_rating_div)
        comment_rating_div.append(comment_rating)

        // Render SPAN content
        const comment_content_div = document.createElement("div")
        const comment_content = document.createElement("span")
        comment_content_div.setAttribute("class", "comment-content-box")
        comment_content.setAttribute("class" ,"comment-content")
        comment_content.innerText = "Content: " + comment.content
        comment_info_div.append(comment_content_div)
        comment_content_div.append(comment_content)

        // Render BUTTON delete
        const delete_button_div = document.createElement("div")
        const delete_button = document.createElement("button")
        delete_button_div.setAttribute("class", "delete-button-box")
        delete_button_div.setAttribute("class", "delete-button")
        delete_button.innerText = "Delete"
        delete_button.onclick = function (){
            delete_comment(DOM, comment.comment_id)
        }
        comment_info_div.append(delete_button_div)
        delete_button_div.append(delete_button)
    }
}