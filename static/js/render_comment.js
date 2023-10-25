function render_comment(data){
    for (let i = 0; i < data.length; i++) {
        const comment = data[i];

        const comment_div = document.createElement("div");

        comment_div.setAttribute("class", "comment");

        $(".comment-box").append(comment_div);

        const commenter_window = render_commenter_window(comment_div, comment)

        comment_div.onmouseover = function (){
            commenter_window.style.display = "block";
        }
        comment_div.onmouseout = function (){
            commenter_window.style.display = "none";
        }
        
        const commenter_img_div = document.createElement("div");
        const commenter_img = document.createElement("img");

        commenter_img_div.setAttribute("class", "commenter-name");
        commenter_img.setAttribute("src", comment.user_image);

        commenter_img_div.append(commenter_img);
        comment_div.append(commenter_img_div);

        const commenter_name_div = document.createElement("div");
        const commenter_name = document.createElement("span");

        commenter_name_div.setAttribute("class", "commenter-name");
        commenter_name.innerText = "name: " + comment.commenter_name;

        commenter_name_div.append(commenter_name);
        comment_div.append(commenter_name_div);

        const comment_content_div = document.createElement("div");
        const comment_content = document.createElement("span");

        comment_content_div.setAttribute("class", "comment-text");
        comment_content.innerText = "content: " + comment.content;

        comment_content_div.append(comment_content);
        comment_div.append(comment_content_div);
    }
}


function render_commenter_window(comment_div, comment) {
    const commenter_window = document.createElement("div");

    commenter_window.setAttribute("class", "commenter-window");

    const commenter_img_div = document.createElement("div");
    const commenter_img = document.createElement("img");

    commenter_img_div.setAttribute("class", "commenter-img-window");
    commenter_img.setAttribute("src", comment.user_image);

    commenter_img_div.append(commenter_img);
    comment_div.append(commenter_img_div);

    const commenter_name_div = document.createElement("div");
    const commenter_name = document.createElement("span");

    commenter_name_div.setAttribute("class", "commenter-name-window");
    commenter_name.innerText = "name: " + comment.commenter_name;

    commenter_name_div.append(commenter_name);
    comment_div.append(commenter_name_div);

    const commenter_introduction_div = document.createElement("div");
    const commenter_introduction = document.createElement("span");

    commenter_introduction_div.setAttribute("class", "commenter-name");
    commenter_introduction.innerText = "introduction: " +  get_introduction(comment.comment_id);

    commenter_introduction_div.append(commenter_introduction);
    comment_div.append(commenter_introduction_div);

    return commenter_window;
}

function get_introduction(comment_id){
    let introduction = ""
    $.ajax({
        url:"/comment/getIntroductionByCommentID",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data: {comment_id:comment_id},
        success:function (data){
            introduction = data.introduction;
        },
    })
    return introduction;
}