/**
 *
 * @param DOM container
 * @param type
 */
function render_log(DOM, type){
    $.ajax({
        url:"log/get_log",
        type:"get",
        data:{
            admin_phone,
            type:type
        },
        success: function (data){
            console.log(data)
            render_data(DOM, data)
        }
    })
}

function render_data(DOM, data){
    DOM.empty();

    for (let i=0; i<data.length; i++){

        const log = data[i]

        // Render DIV log
        const log_box = document.createElement("div");
        log_box.setAttribute("class", "log")
        DOM.append(log_box)

        // Render SPAN log type
        const log_type = document.createElement("span")
        log_type.setAttribute("class", "log-type")
        log_type.innerText = log.log_type
        log_box.append(log_type)

        // Render SPAN log time
        const log_time = document.createElement("span")
        log_time.setAttribute("class", "log-time")
        log_time.innerText = log.log_time
        log_box.append(log_time)

        // Render SPAN log phone
        const log_phone = document.createElement("span")
        log_phone.setAttribute("class", "log-phone")
        log_phone.innerText = log.phone
        log_box.append(log_phone)

        // Render SPAN log content
        const log_content = document.createElement("span")
        log_content.setAttribute("class", "log-content")
        log_content.innerText = log.log_content
        log_box.append(log_content)
    }


}