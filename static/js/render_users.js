/**
 * This function will render users at users_box
 */
function render_users(){
    $.ajax({
        url:"/administer/getUser",
        type:"get",
        data:{admin_phone: admin_phone},
        success:function (data){
            if (data.success){
                render_data(data);
            }else {
                console.log(data.message)
            }
        }
    })
}

function render_data(data){
    users_box.empty();

    for (let i=0; i<data; i++){
        const user = data[i]
        // Render DIV image
        const image_div = document.createElement("div")
        const image = document.createElement("img")
        phone_div.setAttribute("class", "image-box")
        phone.setAttribute("class", "image")
        image.setAttribute("src", user.image_src);
        users_box.append(image_div);
        image_div.append(image);

        // Render DIV phone
        const phone_div = document.createElement("div")
        const phone = document.createElement("span")
        phone_div.setAttribute("class", "phone-box")
        phone.setAttribute("class", "phone")
        phone.innerText = user.phone
        users_box.append(phone_div);
        phone_div.append(phone);

        // Render DIV user type
        const user_type_div = document.createElement("div")
        const user_type_span = document.createElement("span")
        user_type_div.setAttribute("class", "user-type-box")
        user_type_span.setAttribute("class", "user-type")
        user_type.innerText = user.user_type
        users_box.append(user_type_div)
        user_type_div.append(user_type_span)

        // Render DIV status
        const status_div = document.createElement("div")
        const status = document.createElement("span")
        status_div.setAttribute("class", "status-box")
        status.innerText = user.status
        users_box.append(status_div);
        status_div.append(status);

        const jump_div = document.createElement("div")
        const jump_button = document.createElement("button")
        jump_div.setAttribute("class", "jump-box")
        jump_button.setAttribute("class", "jump-button")
        jump_button.setAttribute("type", "button")
        jump_button.onclick = function (){
            window.location.href = user_type==="1"?"/buyerManage":"/sellerManage" + "?phone=" + user.phone;
        }
        jump_button.innerText = "detail"
        users_box.append(jump_div)
        jump_div.append(jump_button)
    }
}
