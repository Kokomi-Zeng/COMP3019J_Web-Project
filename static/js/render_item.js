/**
 * This method is to render Products depend on products data
 * This method will render items in "item_container"
 * @param data is JSON that contains items info
 */
function render_item(data){

    for (let i=0; i<data.length; i++){
        // get each item
        const item = data[i];

        // Render DIV container
        const item_box = document.createElement("div");
        item_box.setAttribute("class", "item");


        // Render BUTTON item jump button
        const item_button = document.createElement("button");

        item_button.setAttribute("class", "item-button")
        item_button.onclick = function (){
            window.location.href = "/item?product_id="+ item.product_id;
        }
        item_container.append(item_box);
        item_box.append(item_button);


        // Render IMG img
        const img_box = document.createElement("div");
        const img = document.createElement("img");

        img_box.setAttribute("class", "img-box");
        img.setAttribute("src", item.image_src);

        item_button.append(img_box);
        img_box.append(img);


        // Rendder SPAN price
        const price_box = document.createElement("div");
        const price = document.createElement("span");

        img_box.setAttribute("class", "price-box");
        price.innerText = "Price: " + item.price;

        item_box.append(price_box);
        price_box.append(price);


        // Render SPAN name
        const name_box = document.createElement("div");
        const name = document.createElement("span");

        img_box.setAttribute("class", "name-box");
        name.innerText = "Name: " + item.product_name;

        item_box.append(name_box);
        name_box.append(name);


        // Render SPAN rati
        const rating_box = document.createElement("div");
        const rating = document.createElement("span");

        img_box.setAttribute("class", "rating-box");
        rating.innerText = "Rating: " + item.rating;

        item_box.append(rating_box);
        rating_box.append(rating);

    }
}