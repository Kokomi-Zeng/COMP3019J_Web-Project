function render_self_comment_box() {
    const self_comment_box = $(".self-comment-box");
    self_comment_box.empty();

    const self_comment_form = document.createElement("form");

    self_comment_form.setAttribute("id", "self-comment")

    self_comment_box.append(self_comment_form)

    const self_rating_div = document.createElement("div");
    const self_rating = document.createElement("input");

    self_rating_div.setAttribute("class", "self-rating-box");
    self_rating.setAttribute("class", "self-rating");
    self_rating.setAttribute("placeHolder", "rating");
    self_rating.setAttribute("type", "number");

    self_comment_form.append(self_rating_div);
    self_rating_div.append(self_rating);

    const self_content_div = document.createElement("div");
    const self_content = document.createElement("input");

    self_content_div.setAttribute("class", "self-content-box");
    self_content.setAttribute("class", "self-content");
    self_content.setAttribute("placeHolder", "content");
    self_rating.setAttribute("type", "text");

    self_comment_form.append(self_content_div);
    self_content_div.append(self_content);

    const self_content_button = document.createElement("button");

    self_content_button.setAttribute("id", "self-content-button");
    self_content_button.innerText = "Submit->"
    self_content_button.onclick = function () {
        create_comment(new FormData(self_comment_form))
    }

    self_comment_box.append(self_content_button);

}

function create_comment(formdata){
    $.ajax({
        url: "/comment/createComment",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data: formdata,
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
