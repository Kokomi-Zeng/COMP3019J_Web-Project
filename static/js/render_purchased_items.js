/**
 * This method will render data in "purchased_item_box"
 * @param data
 */
function render_purchased_items(data){

    //clear DOM
    purchased_item_box.empty();

    console.log("data length: " + data.length)
    for (let i = 0; i<data.length; i++) {
        // get each item
        const item = data[i];

        // Render DIV item container
        const item_div = document.createElement("div");
        item_div.setAttribute("class", "item-box");
        purchased_item_box.append(item_div);

        const item_img_div = document.createElement("div");
        const item_img = document.createElement("img");

        item_img_div.setAttribute("class", "item-img-box");
        item_img.setAttribute("src", item.image_src);

        item_img_div.append(item_img);
        item_div.append(item_img_div);

        // Render SPAN item name
        const item_name_div = document.createElement("div");
        const item_name = document.createElement("span");

        item_name_div.setAttribute("class", "item-name-box");
        item_name.innerText = item.product_name;

        item_name_div.append(item_name);
        item_div.append(item_name_div);

        // Render SPAN item quantity
        const item_quantity_div = document.createElement("div");
        const item_quantity = document.createElement("span");

        item_quantity_div.setAttribute("class", "item-quantity-box");
        item_quantity.innerText = item.purchase_quantity;

        item_quantity_div.append(item_quantity);
        item_div.append(item_quantity_div);

        // Render SPAN purchased time
        const item_time_div = document.createElement("div");
        const item_time = document.createElement("span");

        item_time_div.setAttribute("class", "item-time-box");
        item_time.innerText = item.purchase_time;

        item_time_div.append(item_time);
        item_div.append(item_time_div);

        // Render SPAN total price
        const item_price_div = document.createElement("div");
        const item_price = document.createElement("span");

        item_price_div.setAttribute("class", "item-price-box");
        item_price.innerText = item.total_price;

        item_price_div.append(item_price);
        item_div.append(item_price_div);
    }
}