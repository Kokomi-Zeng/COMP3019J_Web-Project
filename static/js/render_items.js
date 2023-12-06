/**
 * This method is to render Products depend on products data
 * This method will render items in "item_container"
 * @param data is JSON that contains items info
 * @param type
 */
function render_items(data, type){

    for (let i=0; i<data.length; i++){
        // get each item
        const item = data[i];

        // Render DIV container
        const item_box = document.createElement("div");
        item_box.setAttribute("class", "item");


        // Render BUTTON item jump button
        const item_button = document.createElement("button");

        item_button.setAttribute("class", "item-button")
        item_button.setAttribute("type", "button")
        item_button.onclick = function (){
            if (isAdmin){
                window.location.href = "/itemManage?product_id="+ item.product_id;
            } else if (type==="1"){
                window.location.href = "/itemBuyer?product_id="+ item.product_id;
            } else if (type==="0"){
                window.location.href = "/itemSeller?product_id="+ item.product_id;
            } else {
                window.location.href = "/item?product_id="+ item.product_id;
            }
        }
        item_container.append(item_box);
        item_box.append(item_button);

        // Render IMG img
        const img_box = document.createElement("div");
        const img = document.createElement("img");

        img_box.setAttribute("class", "img-box");
        img.setAttribute("src", item.image_src);

        item_box.append(img_box)
        img_box.append(item_button);
        item_button.append(img);

        // Render DIV item info box
        const item_info_box = document.createElement("div")
        item_info_box.setAttribute("class", "item-info-box")
        item_box.append(item_info_box)

        // Render SPAN price
        const price_box = document.createElement("div");
        const price = document.createElement("span");

        price_box.setAttribute("class", "price-box");
        price.innerText = "Price: " + item.price;

        item_info_box.append(price_box);
        price_box.append(price);


        // Render SPAN name
        const name_box = document.createElement("div");
        const name = document.createElement("span");

        name_box.setAttribute("class", "name-box");
        name.innerText = "Name: " + item.product_name;

        item_info_box.append(name_box);
        name_box.append(name);


        // Render SPAN rati
        const rating_box = document.createElement("div");
        const rating = document.createElement("span");

        rating_box.setAttribute("class", "rating-box");
        rating.innerText = "Rating: " + item.rating;

        item_info_box.append(rating_box);
        rating_box.append(rating);

    }
}