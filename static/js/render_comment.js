function render_self_comment() {
    const comment_box = $(".self-comment-box");
    comment_box.empty();

    const self_rating_div = document.createElement("div");
    const self_rating = document.createElement("input");

    self_rating_div.setAttribute("class", "self-rating-box");
    self_rating.setAttribute("class", "self-rating");
    self_rating.setAttribute("placeHolder", "rating");
    self_rating.setAttribute("type", "number");


    const self_content_div = document.createElement("div");
    const self_content = document.createElement("input");

    self_content_div.setAttribute("class", "self-content-box");
    self_content.setAttribute("class", "self-content");
    self_content.setAttribute("placeHolder", "content");
    self_rating.setAttribute("type", "text");


    const self_content_button = document.createElement("button");

    self_content_button.setAttribute("id", "self-content-button");
    self_content_button.innerText = "Submit->"
    self_content_button.onclick = function () {
        console.log(self_rating.value)
        console.log(self_content.value)
        $.ajax({
            url: "/comment/createComment",
            type: "get",
            contentType: "application/json",
            dataType: "json",
            data: {
                buyer_phone: phone,
                content: self_content.value,
                rating: self_rating.value,
                product_id: "{{ product_id }}"
            },
            success:function (data){
                if (data.success){
                    alert(data.message)
                    render_comment();
                }else {
                    alert(data.message)
                }
            }
        })
    }
    self_content_div.append(self_content);
    self_rating_div.append(self_rating);
    comment_box.append(self_rating_div);
    comment_box.append(self_content_div);
    comment_box.append(self_content_button);

}

function render_comment(data){
    for (let i = 0; i < data.length; i++) {
        const comment = data[i];
        const comment_div = document.createElement("div");
        comment_div.setAttribute("class", "comment");
        comment_div.onmouseover = function (){
            comment_div.style.display = "block";
        }
        comment_div.onmouseout = function (){
            comment_div.style.display = "none";
        }

        const comment_rating_div = document.createElement("div");
        const comment_rating = document.createElement("span");

        comment_rating_div.setAttribute("class", "comment-rating");
        comment_rating.innerText = comment.rating;

        comment_rating_div.append(comment_rating);
        comment_div.append(comment_rating_div);

        const comment_content_div = document.createElement("div");
        const comment_content = document.createElement("span");

        comment_content_div.setAttribute("class", "comment-text");
        comment_content.innerText = comment.content;

        comment_content_div.append(comment_content);
        comment_div.append(comment_content_div);

        const comment_text = document.createComment("div");
        comment_text.innerText = comment.text;

        $(".item-comment-box").append(comment_div);
    }
}


