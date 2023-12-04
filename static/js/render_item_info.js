/**
 * This function will render at info_box & rating_box
 * @param data is data
 */
function render_item_info(data){

    const img_div = document.createElement("div", {
        class:"item-imm-box"
    })
    const img = document.createElement("img", {
        class:"item-img"
    });
    img.setAttribute("src", data.image_src);
    info_box.append(img_div)
    img_div.append(img)

    const name_div = document.createElement("div", {
        class:"item-name-box"
    })
    info_box.append(name_div)

    const description_div = document.createElement("div", {
        class:"item-description-box"
    })
    info_box.append(description_div)

    const price_div = document.createElement("div", {
        class:"item-price-box"
    })
    info_box.append(price_div)

    const storage_div = document.createElement("div", {
        class:"item-storage-box"
    })
    info_box.append(storage_div)

    const rating_span = document.createElement("span", {
        class:"item-rating"
    })
    rating_span.innerText = data.average_rating;
    rating_box.append(rating_span)

    if (!belong) {
        // buyer
        const name_span = document.createElement("span", {
            id:"item-name"
        });
        name_span.innerText ="Name: " + data.name;

        const price_span = document.createElement("span", {
            id:"item-price"
        });
        price_span.innerText ="Price: " + data.price;

        const storage_span = document.createElement("span", {
            id:"item-storage"
        });
        storage_span.innerText ="Storage: " + data.storage;

        const description_span = document.createElement("p", {
            id:"item-description"
        });
        description_span.innerText ="description: " + data.description;

    }else {
        // seller
        const img_form = document.createElement("form", {
            class: "img-form"
        })
        img_form.style.display = "None";
        const img_input = document.createElement("input", {
            type:"file",
            id:"img-input",
            accept:"image/*",
        })
        const img_a = document.createElement("a", {
            class:"item-img-a"
        })

        img_input.onchange = function (){
            update_item_image(new FormData(img_form));
        }
        img.onclick = function (){
            img_input.click();
        }
        img_div.append(img_form)
        img_div.append(img_a)
        img_a.append(img)
        img_form.append(img_input);

        const name_input = document.createElement("input", {
            type:"text",
            value:"Name: " + data.name,
            id:"item-name"
        });
        name_input.onblur = update_item_msg();
        name_div.append(name_input)

        const price_input = document.createElement("input", {
            type:"text",
            value:"Price: " + data.price,
            id:"item-price"
        });
        price_input.onblur = update_item_msg();
        price_div.append(price_input)

        const storage_input = document.createElement("input", {
            type:"text",
            value:"Storage: " + data.storage,
            id:"item-storage"
        });
        storage_input.onblur = update_item_msg();
        storage_div.append(storage_input)

        const description_span = document.createElement("textarea", {
            id:"item-description",
        });
        description_span.innerText = "description: " + data.description;
        description_span.onblur = update_item_msg();
        description_div.append(description_span)
    }
}

function update_item_image(formdata, product_id){
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