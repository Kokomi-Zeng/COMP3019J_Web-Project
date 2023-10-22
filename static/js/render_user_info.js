function render_user_info(data) {

    const container = $(".container");
    container.empty();

    // input img
    const img_div = document.createElement("div");
    const img_show = document.createElement("img");
    const img_input = document.createElement("input");

    img_div.setAttribute("class", "info-div");
    img_div.setAttribute("id", "name-div");
    img_show.setAttribute("id", "show-img");
    img_input.setAttribute("type", "file");
    img_input.setAttribute("id", "img");

    name_div.append(name_label);
    name_label.append(name_input)
    container.append(name_div);

    // name
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
    container.append(name_div);

    // phone
    const phone_div = document.createElement("div");
    const phone_span = document.createElement("label")

    phone_div.setAttribute("class", "info-div");
    phone_div.setAttribute("id", "phone-div");
    phone_span.innerText = "Phone: " + phone;

    phone_div.append(phone_span);
    container.append(phone_div);

    // introduction

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
    container.append(introduction_div);

    // password

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
    container.append(password_div);

    // submit
    const submit_div = document.createElement("div");
    const submit_button = document.createElement("button");

    submit_button.innerText = "Confirm";
    submit_button.onclick = function () {
        modify_user_info(name_input.value, password_input.value, introduction_input.value)
    }
    submit_div.append(submit_button);
    container.append(submit_div);
}

function modify_user_info(name, password, introduction){
    $.ajax({
        url: type==="1"?"/buyer/modifyBuyerInfo":'/seller/modifySellerInfo',
        type: 'get',
        contentType: "application/json",
        dataType: "json",
        data: {
            phone: phone,
            name: name,
            password: password,
            introduction: introduction,
        },
        success: function (data) {
            if (data.success) {
                render_user_info();
            }else {
                alert(data.message);
            }
        }
    })
}

function get_user_img(show_img){
    $.ajax({
        url:"/images/get_image_user",
        type: 'get',
        contentType: "application/json",
        dataType: "json",
        data:{
            phone:phone,
        },
        success:function (data){
            show_img.setAttribute("src", data.url);
        }
    })
}

function upload_user_img(show_img){
    $.ajax({
        url:"/images/upload_image_user",
        type:"post",
        data:{
            file:$("#file")[0].files[0],
            phone:"{{ product_id }}",
        },
        dataType:"text",
        processData:false,
        contentType:false,
        success:function (data){
            show_img.setAttribute("src", data.src)
        }
    })
}