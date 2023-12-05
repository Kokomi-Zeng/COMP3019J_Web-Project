/**
 * This method is to render user info depend on the ajax response.
 * This method render data in $(".user-info-box")
 * @param data is the ajax response.
 */
function render_user_info(data) {

    // clear DOM
    user_info_box.empty();

    // Render FORM for img
    const img_form = document.createElement("form");
    img_form.setAttribute("class", "img-form");
    // Render INPUT FILE img
    const img_div = document.createElement("div");
    const img_show = document.createElement("img");
    const img_input = document.createElement("input");

    img_div.setAttribute("class", "info-div");
    img_div.setAttribute("id", "img-div");
    img_form.style.alignItems = "center";
    img_show.setAttribute("class", "user-image");
    img_show.setAttribute("width", "300px")
    img_show.setAttribute("height", "300px")

    img_input.setAttribute("type", "file");
    img_input.setAttribute("id", "file");
    img_input.setAttribute("name", "image");
    img_input.setAttribute("accept", "image/*");
    img_input.onchange = function (){
        const formdata = new FormData(img_form);
        // formdata.append("phone", phone);
        console.log(formdata)
        upload_user_img(formdata);
    }

    img_form.append(img_show);
    img_form.append(img_input)
    img_div.append(img_form);
    user_info_box.append(img_div);

    // Render INPUT TEXT name
    const name_div = document.createElement("div");
    const name_label = document.createElement("label")
    const name_input = document.createElement("input");

    name_div.setAttribute("class", "info-div");
    name_div.setAttribute("id", "name-div");
    name_label.innerText = "Name: "
    name_input.setAttribute("type", "text");
    name_input.setAttribute("value", data.name);
    name_input.setAttribute("id", "name");

    name_div.append(name_label);
    name_label.append(name_input)
    user_info_box.append(name_div);

    // Render INPUT TEXT phone
    const phone_div = document.createElement("div");
    const phone_span = document.createElement("label")

    phone_div.setAttribute("class", "info-div");
    phone_div.setAttribute("id", "phone-div");
    phone_span.innerText = "Phone: " + phone;

    phone_div.append(phone_span);
    user_info_box.append(phone_div);

    // Render INPUT TEXT introduction

    const introduction_div = document.createElement("div");
    const introduction_label = document.createElement("label")
    const introduction_input = document.createElement("input");

    introduction_div.setAttribute("class", "info-div");
    introduction_div.setAttribute("id", "introduction-div");
    introduction_label.innerText = "Introduction: ";
    introduction_input.setAttribute("type", "text");
    introduction_input.setAttribute("value", data.introduction);
    introduction_input.setAttribute("id", "introduction");

    introduction_div.append(introduction_label);
    introduction_label.append(introduction_input);
    user_info_box.append(introduction_div);


    // Render INPUT PASSWORD password
    const password_div = document.createElement("div");
    const password_label = document.createElement("label")
    const password_input = document.createElement("input");

    password_div.setAttribute("class", "info-div");
    password_div.setAttribute("id", "password-div");
    password_label.innerText = "Password: ";
    password_input.setAttribute("type", "text");
    password_input.setAttribute("id", "password");

    password_div.append(password_label);
    password_label.append(password_input);
    user_info_box.append(password_div);


    // Render BUTTON submit
    const submit_div = document.createElement("div")
    const submit_button = document.createElement("button");

    submit_div.setAttribute("class", "submit-box");
    submit_button.innerText = "Confirm";
    submit_button.onclick = function () {
        modify_user_info(name_input.value, password_input.value, introduction_input.value)
    }
    submit_div.append(submit_button);
    user_info_box.append(submit_div);

    get_user_image($(".user-image"));
}

/**
 * This method is to modify user information.
 * @param name is the user name after modified.
 * @param introduction is the introduction after modified.
 * @param password is password that promise the security of this modification.
 */
function modify_user_info(name, introduction, password){
    $.ajax({
        url: type==="1"?"/buyer/modifyBuyerInfo":'/seller/modifySellerInfo',
        type: 'post',
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            phone: phone,
            name: name,
            password: password,
            introduction: introduction,
        }),
        success: function (data) {
            if (data.success) {
                alert(data.message);
                render_user_info(data)
            }else {
                alert(data.message);
            }
        }
    })
}

/**
 * This method is to upload user image.
 * @param formdata is the Formdata object that contains information of user image.
 */
function upload_user_img(formdata){
    $.ajax({
        url:"/images/upload_image_user?phone="+phone,
        type:"post",
        data:formdata,
        dataType:"json",
        processData:false,
        contentType:false,
        success:function (data){
            if (data.success) {
                get_user_image($(".user-image"));
            }else {
                alert(data.message);
            }
        }
    })
}