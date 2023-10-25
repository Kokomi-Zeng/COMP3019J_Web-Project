function alert_message(message){
    $("#alert-message").text(message);
    const window = $(".alert")
    window_appear(window);
}

function window_appear(window){
    window.css("display", "block");
    setTimeout(() =>window.css("display", "none") , 3000);
}
