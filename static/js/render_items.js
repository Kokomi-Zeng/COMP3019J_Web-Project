/**
 * This method is to render Products depend on products data
 * This method will render items in "item_container"
 * @param DOM
 * @param data is JSON that contains items info
 */
function render_items(DOM, data){

    for (let i=0; i<data.length; i++){
        // get each item
        const item = data[i];

        // Render DIV container
        const item_div = document.createElement("div");
        item_div.setAttribute("class", "item");


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
        DOM.append(item_div);
        item_div.append(item_button);

        // Render IMG img
        const img_div = document.createElement("div");
        const img = document.createElement("img");

        img_div.setAttribute("class", "img-box");
        img.setAttribute("src", item.image_src);

        item_div.append(img_div)
        img_div.append(item_button);
        item_button.append(img);

        // Render DIV item info box
        const item_info_div = document.createElement("div")
        item_info_div.setAttribute("class", "item-info-box")
        item_div.append(item_info_div)

        // Render SPAN price
        const price_div = document.createElement("div");
        const price = document.createElement("span");

        price_div.setAttribute("class", "price-box");
        price.innerText = "Price: " + item.price;

        item_info_div.append(price_div);
        price_div.append(price);


        // Render SPAN name
        const name_div = document.createElement("div");
        const name = document.createElement("span");

        name_div.setAttribute("class", "name-box");
        name.innerText = "Name: " + item.product_name;

        item_info_div.append(name_div);
        name_div.append(name);


        // Render SPAN rating
        const rating_div = document.createElement("div");
        const rating = document.createElement("span");

        rating_div.setAttribute("class", "rating-box");
        rating.innerText = "Rating: " + item.rating;

        item_info_div.append(rating_div);
        rating_div.append(rating);
    }
}