/**
 * This function will render at info_box & rating_box
 * @param product_id is product id
 */
function render_item_info(product_id){
    $.ajax({
        url:"/products/itemInfoById",
        type:"get",
        data:{product_id: product_id},
        success: function (data){
            $("#item-img").attr("src", data.image_src);

            // SPAN
            $("#item-price").text(data.price);
            $("#item-name").text(data.name)
            $("#item-storage").text(data.storage);
            $("#item-description").text(data.description);
            $("#item-rating").text(data.average_rating);

            // INPUT
            $("#item-name").val(data.name)
            $("#item-storage").val(data.storage);
            $("#item-description").val(data.description);
            $("#item-rating").val(data.average_rating);
            $("#item-price").val(data.price);
        }
    })

    // const img_div = document.createElement("div")
    // const img = document.createElement("img");
    // img_div.setAttribute("class", "item-img-box")
    // img.setAttribute("class", "item-img")
    // img.setAttribute("src", data.image_src);
    // info_box.append(img_div)
    // img_div.append(img)
    //
    // const name_div = document.createElement("div")
    // name_div.setAttribute("class", "item-name-box")
    // info_box.append(name_div)
    //
    // const description_div = document.createElement("div")
    // description_div.setAttribute("class", "item-description-box")
    // info_box.append(description_div)
    //
    // const price_div = document.createElement("div")
    // price_div.setAttribute("class", "item-price-box")
    // info_box.append(price_div)
    //
    // const storage_div = document.createElement("div")
    // storage_div.setAttribute("class", "item-storage-box")
    // info_box.append(storage_div)
    //
    // const rating_span = document.createElement("span")
    // storage_div.setAttribute("class", "item-rating")
    // rating_span.innerText = data.average_rating;
    // rating_box.append(rating_span)
    //
    // if (!belong) {
    //     // buyer
    //     const name_span = document.createElement("span");
    //     name_span.innerText ="Name: " + data.name;
    //     name_div.append(name_span)
    //
    //     const price_span = document.createElement("span");
    //     price_span.innerText ="Price: " + data.price;
    //     price_div.append(price_span)
    //
    //     const storage_span = document.createElement("span")
    //     storage_span.innerText ="Storage: " + data.storage;
    //     storage_div.append(storage_span)
    //
    //     const description_span = document.createElement("span")
    //     description_span.innerText ="description: " + data.description;
    //     description_div.append(description_span)
    //
    // }else {
    //     // seller
    //     const img_form = document.createElement("form")
    //     const img_input = document.createElement("input")
    //     const img_button = document.createElement("button")
    //
    //     img_form.setAttribute("class", "img-form")
    //     img_form.style.display = "None";
    //     img_input.setAttribute("type", "file")
    //     img_input.setAttribute("id", "img-input")
    //     img_input.setAttribute("name", "file")
    //     img_input.setAttribute("accept", "image/*")
    //     img_input.onchange = function (){
    //         update_item_image(new FormData(img_form), data.product_id);
    //     }
    //     img_button.setAttribute("class", "img-button")
    //     img_button.setAttribute("type", "button")
    //     img_button.onclick = function (){
    //         img_input.click();
    //     }
    //     img.onclick = function (){
    //         img_input.click();
    //     }
    //     img_div.append(img_form)
    //     img_div.append(img_button)
    //     img_button.append(img)
    //     img_form.append(img_input);
    //
    //     const name_input = document.createElement("input")
    //     name_input.setAttribute("class", "item-name")
    //     name_input.setAttribute("type", "text")
    //     name_input.setAttribute("value", "Name: " + data.name)
    //     name_input.onblur = function (){
    //         update_item_msg(name_input.value, price_input.value, storage_input.value, description_textarea.value);
    //     }
    //
    //     name_div.append(name_input)
    //
    //     const price_input = document.createElement("input")
    //     price_input.setAttribute("class", "item-price")
    //     price_input.setAttribute("type", "text")
    //     price_input.setAttribute("value", "Price: " + data.price)
    //     price_input.onblur = function (){
    //         update_item_msg(name_input.value, price_input.value, storage_input.value, description_textarea.value);
    //     }
    //     price_div.append(price_input)
    //
    //     const storage_input = document.createElement("input")
    //     price_input.setAttribute("class", "item-storage")
    //     price_input.setAttribute("type", "text")
    //     price_input.setAttribute("value", "Storage: " + data.storage)
    //     storage_input.onblur = function (){
    //         update_item_msg(name_input.value, price_input.value, storage_input.value, description_textarea.value);
    //     }
    //     storage_div.append(storage_input)
    //
    //     const description_textarea = document.createElement("textarea")
    //     description_textarea.setAttribute("class", "item-description")
    //     description_textarea.innerText = "description: " + data.description;
    //     description_textarea.onblur = function (){
    //         update_item_msg(name_input.value, price_input.value, storage_input.value, description_textarea.value);
    //     }
    //     description_div.append(description_textarea)
    // }
}

function update_item_image(formdata){
    $.ajax({
        url:"/images/upload_image_product?product_id=" + product_id,
        type:"post",
        data:formdata,
        dataType:"json",
        processData:false,
        contentType:false,
        success:function (data){
            if (!data.success) {
                alert(data.message);
            }else{
                get_and_render_item_data()
            }
        }
    })
}

function update_item_msg(name, price, storage, description){
        $.ajax({
            url:"/products/modifyItem",
            type:"get",
            data:{
                seller_phone: phone,
                product_name: name,
                description: description,
                product_id: product_id,
                price: price,
                storage: storage,
            }
        })
    }