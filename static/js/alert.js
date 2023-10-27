/**
 * this method attempts to replace "alert()" to have a better UI.
 * make the window visible.
 * @param message is the String text that you want alert
 */
function alert_message(message){
    $("#alert-message").text(message);
    const window = $(".alert")
    window_appear(window);
}

/**
 * this method is only used by function "alert_message".
 * make the window invisible.
 * @param window is the window that need to be invisible
 */
function window_appear(window){
    window.css("display", "block");
    setTimeout(() =>window.css("display", "none") , 3000);
}
