/**
 * This method is to render user info depend on the ajax response.
 * This method render data in user_info_box, user_amount_box
 * need type, phone
 */
function render_user_info() {
    get_and_render_user_basic_data()
    if (type==="1"){
        get_and_render_money()
    }
}

function get_and_render_user_basic_data(){
    $.ajax({
        url: type==="1"?"/buyer/buyerInfo":"/seller/sellerInfo",
        type: 'get',
        contentType: "application/json",
        dataType: "json",
        data:{
            phone: phone
        },
        success:function (data){
            render_user_basic_data(data)
        }
    })
}

function get_and_render_money() {
    $.ajax({
        url: "/buyer/getMoney",
        type: "get",
        contentType: "application/json",
        dataType: "json",
        data: {
            phone: phone,
        },
        success: function (data) {
            render_money(data);
        }
    })
}
    
function render_user_basic_data(data){
    $("#introduction").val(data.introduction)
    $("#name").val(data.name)
    $("#phone").innerText = phone;
}

    // Render SPAN current money
function render_money(data){

    // clear DOM
    user_amount_box.empty();

    // Render SPAN current money
    const current = data.money;
    const current_div = document.createElement("div");
    const current_span = document.createElement("span");

    current_div.setAttribute("class", "charge-div");
    current_div.setAttribute("id", "current-div");
    current_span.innerText = "Current: "+current;

    current_div.append(current_span);
    user_amount_box.append(current_div);

    // Render FORM
    const pay_form = document.createElement("form", {
        class: "pay-form",
    })
    user_amount_box.append(pay_form);

    // Render INPUT NUMBER current money
    const pay_div = document.createElement("div");
    const pay_input = document.createElement("input", {
        id:"pay",
        type:"number",
        placeHolder:"recharge amount",
        name:"charge_num"
    });

    pay_div.append(pay_input);
    pay_form.append(pay_div);

    // Render INPUT PASSWORD password
    const password_div = document.createElement("div", {
        class:"charge-div",
        id:"password-div"
    });
    const password_input = document.createElement("input", {
        type:"password",
        id:"password",
        placeHolder:"password",
        name:"password"
    });

    password_div.append(password_input);
    pay_form.append(password_div);

    // Render BUTTON purchase
    const submit_div = document.createElement("div");
    const submit_button = document.createElement("button");

    submit_button.innerText = "Purchase"
    submit_button.setAttribute("class", "charge-button")
    submit_button.onclick = function (){
        if (type===1){
            charge();
        }else if (type===2){
            modify_amount();
        }
    }
    submit_div.append(submit_button);
    user_amount_box.append(submit_div);
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
            introduction: introduction,
            password: password
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

function charge(){
    const formdata = new FormData($(".pay-form")[0]);
    formdata.append("phone", phone);
    $.ajax({
        url:'/buyer/charge',
        type:'get',
        contentType: "application/json",
        dataType: "json",
        data:formdata,
        success:function (data){
            alert(data.message)
            if (data.success) {

                get_and_render_money();
            }
        }
    })
}

function modify_amount(){
    const formdata = new FormData($(".pay-form")[0]);
}

/**
 * This method is to upload user image.
 * @param formdata is the Formdata object that contains information of user image.
 */
function upload_user_img(formdata){
    $.ajax({
        url:"/images/upload_image_user",
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