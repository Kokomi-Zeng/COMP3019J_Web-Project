/**
 * This function is for admin to render all purchased messages
 * @param DOM is JQuery Selector where purchased messages are loaded
 */
function render_all_purchased_items(DOM){
    $.ajax({
        url:"buyer/getAllBuyerItem",
        type:"get",
        success:function (data){
            render_data(DOM, data)
        }
    })
}

function render_data(DOM, data){

    //clear DOM
    DOM.empty();

    console.log("data length: " + data.length)
    for (let i = 0; i<data.length; i++) {
        // get each item
        const item = data[i];

        // Render DIV item container
        const item_div = document.createElement("div");
        item_div.setAttribute("class", "item-box");
        DOM.append(item_div);

        // Render IMG image
        const item_img_div = document.createElement("div");
        const item_img = document.createElement("img");

        item_img_div.setAttribute("class", "item-img-box");
        item_img.setAttribute("src", item.image_src);

        item_img_div.append(item_img);
        item_div.append(item_img_div);

        // Render DIV info container
        const item_info_div = document.createElement("div")
        item_info_div.setAttribute("class", "item-info-box")
        item_div.append(item_info_div)

        // Render SPAN buyer name
        const purchase_id_div = document.createElement("div");
        const purchase_id = document.createElement("span");
        purchase_id_div.setAttribute("class", "item-img-box");
        purchase_id.setAttribute("src", item.purchase_id);
        purchase_id_div.append(purchase_id);
        item_info_div.append(purchase_id_div);

        // Render SPAN buyer name
        const buyer_name_div = document.createElement("div");
        const buyer_name = document.createElement("span");
        buyer_name_div.setAttribute("class", "buyer-name-box");
        buyer_name.innerText = "Buyer Name: " + item.buyer_name;
        buyer_name_div.append(buyer_name);
        item_info_div.append(buyer_name_div);

        // Render SPAN item name
        const item_name_div = document.createElement("div");
        const item_name = document.createElement("span");

        item_name_div.setAttribute("class", "item-name-box");
        item_name.innerText = "Product Name: " + item.product_name;

        item_name_div.append(item_name);
        item_info_div.append(item_name_div);

        // Render SPAN item quantity
        const item_quantity_div = document.createElement("div");
        const item_quantity = document.createElement("span");

        item_quantity_div.setAttribute("class", "item-quantity-box");
        item_quantity.innerText = "Purchase Quantity: " + item.purchase_quantity;

        item_quantity_div.append(item_quantity);
        item_info_div.append(item_quantity_div);

        // Render SPAN purchased time
        const item_time_div = document.createElement("div");
        const item_time = document.createElement("span");

        item_time_div.setAttribute("class", "item-time-box");
        item_time.innerText = "Purchase Time: " + item.purchase_time;

        item_time_div.append(item_time);
        item_info_div.append(item_time_div);

        // Render SPAN total price
        const item_price_div = document.createElement("div");
        const item_price = document.createElement("span");

        item_price_div.setAttribute("class", "item-price-box");
        item_price.innerText = "Total Price: " + item.total_price;

        item_price_div.append(item_price);
        item_info_div.append(item_price_div);
    }
}