/**
 * This function will render users at users_box
 * need admin_phone
 */
function render_users(){
    $.ajax({
        url:"/administer/getUser",
        type:"get",
        data:{admin_phone: admin_phone},
        success:function (data){
            render_data(data);
        }
    })
}

function render_data(data){
    users_box.empty();

    for (let i=0; i<data.length; i++){
        const user = data[i]
        // Render DIV image
        const image_div = document.createElement("div")
        const image_button = document.createElement("button");
        const image = document.createElement("img")
        image_div.setAttribute("class", "image-box")
        image.setAttribute("class", "image")
        image.setAttribute("src", user.image_src);
        image_button.setAttribute("type", "button")
        image_button.setAttribute("class", "image-button")
        image_button.onclick = function (){
            window.location.href = user.user_type==="1"?"/buyerManage" + "?phone=" + user.phone:"/sellerManage" + "?phone=" + user.phone;
        }
        users_box.append(image_div);
        image_div.append(image_button);
        image_button.append(image)

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
        user_type_span.innerText = user.user_type==="1"?"Buyer":"Seller"
        users_box.append(user_type_div)
        user_type_div.append(user_type_span)

        // Render DIV status
        const status_div = document.createElement("div")
        const status = document.createElement("span")
        status_div.setAttribute("class", "status-box")
        status.innerText = user.status
        users_box.append(status_div);
        status_div.append(status);
    }
}
