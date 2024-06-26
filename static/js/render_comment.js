/**
 * This method is to render the comment data depend on the response.
 * @param DOM is JQuery Selector where comments are loaded
 * @param data is comment data
 */
function render_comment(DOM, data){
    DOM.empty();

    for (let i = 0; i < data.length; i++) {
        let timeoutId;
        const comment = data[i];

        const comment_div = document.createElement("div");

        comment_div.setAttribute("class", "comment");

        DOM.append(comment_div);

        const commenter_window = create_commenter_window(comment)

        comment_div.append(commenter_window);

        // commenter image
        const commenter_img_div = document.createElement("div");
        const commenter_img = document.createElement("img");

        commenter_img_div.setAttribute("class", "commenter-img");
        commenter_img.setAttribute("width", "300px")
        commenter_img.setAttribute("height", "300px")
        commenter_img.setAttribute("src", comment.user_image)

        commenter_img_div.append(commenter_img);

        // commenter window
        // when mouse move on the image, destroy time out
        commenter_img.onmouseover = function() {
            clearTimeout(timeoutId);  // 清除之前的延时
            commenter_window.style.display = "block";
        }

        commenter_img.onmouseout = function() {
            timeoutId = setTimeout(function() {
                commenter_window.style.display = "none";
            }, 100);
        }

        // when mouse move on the window, destroy time out
        commenter_window.onmouseover = function() {
            clearTimeout(timeoutId);
            commenter_window.style.display = "block";
        }

        commenter_window.onmouseout = function() {
            timeoutId = setTimeout(function() {
                commenter_window.style.display = "none";
            }, 100);
        }


        comment_div.append(commenter_img_div);

        // commenter name
        const commenter_name_div = document.createElement("div");
        const commenter_name = document.createElement("span");

        commenter_name_div.setAttribute("class", "commenter-name");
        commenter_name.innerText = "name: " + comment.commenter_name;

        commenter_name_div.append(commenter_name);
        comment_div.append(commenter_name_div);

        // comment rating
        const commenter_rating_div = document.createElement("div");
        const commenter_rating = document.createElement("span");

        commenter_rating_div.setAttribute("class", "commenter-rating");
        commenter_rating.innerText = "Rating: " + comment.rating;

        commenter_rating_div.append(commenter_rating);
        comment_div.append(commenter_rating_div);

        // comment text
        const comment_content_div = document.createElement("div");
        const comment_content = document.createElement("span");

        comment_content_div.setAttribute("class", "comment-text");
        comment_content.innerText = "content: " + comment.content;

        comment_content_div.append(comment_content);
        comment_div.append(comment_content_div);
    }
}

/**
 * This method is to create a commenter window.
 * @param comment is the certain comment data from ajax response.
 * @returns {HTMLDivElement} is a commenter window.
 */
function create_commenter_window(comment) {
    const commenter_window = document.createElement("div");

    commenter_window.setAttribute("class", "commenter-window");

    const commenter_img_div = document.createElement("div");
    const commenter_img = document.createElement("img");

    commenter_img_div.setAttribute("class", "commenter-img-window");
    commenter_img.setAttribute("width", "300px")
    commenter_img.setAttribute("height", "300px")
    commenter_img.setAttribute("src", comment.user_image)

    commenter_img_div.append(commenter_img);
    commenter_window.append(commenter_img_div);

    const commenter_name_div = document.createElement("div");
    const commenter_name = document.createElement("span");

    commenter_name_div.setAttribute("class", "commenter-name-window");
    commenter_name.innerText = "name: " + comment.commenter_name;

    commenter_name_div.append(commenter_name);
    commenter_window.append(commenter_name_div);

    const commenter_introduction_div = document.createElement("div");
    const commenter_introduction = document.createElement("span");

    commenter_introduction_div.setAttribute("class", "commenter-introduction-window");
    commenter_introduction.innerText = "introduction: " +  get_introduction(comment.comment_id);

    commenter_introduction_div.append(commenter_introduction);
    commenter_window.append(commenter_introduction_div);

    return commenter_window;
}

/**
 * This method is to get introduction of the commenter by comment ID.
 * @param comment_id is the comment ID.
 * @returns {string} is the introduction of the certain commenter.
 */
function get_introduction(comment_id){
    let introduction = ""
    $.ajax({
        async: false,
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