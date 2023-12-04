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
        const image_div = document.createElement("div", {
            class:"image-box",
        })
        const image = document.createElement("img", {
            class:"image"
        })
        image.setAttribute("src", user.image_src);
        users_box.append(image_div);
        image_div.append(image);

        // Render DIV phone
        const phone_div = document.createElement("div", {
            class:"phone-box",
        })
        const phone = document.createElement("span", {
            class:"phone"
        })
        phone.innerText = user.phone
        users_box.append(phone_div);
        phone_div.append(phone);

        // Render DIV user type
        const user_type_div = document.createElement("div", {
            class:"user-type-box"
        })
        const user_type = document.createElement("span", {
            class:"user-type"
        })
        user_type.innerText = user.user_type
        users_box.append(user_type_div)
        user_type_div.append(user_type)

        // Render DIV status
        const status_div = document.createElement("div", {
            class:"status-box",
        })
        const status = document.createElement("span", {
            class:"status"
        })
        status.innerText = user.status
        users_box.append(status_div);
        status_div.append(status);
    }
}
