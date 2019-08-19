function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var follow_ajax = false;

$(document).ready(function () {

    $(".follow-btn").click(function () {
        var form = new FormData();
        var button = $(this);
        form.append("user_id", $(this).attr("data-id"));
        console.log(form, "form")
        if (!follow_ajax) {
            follow_ajax = true;
            $.ajax({
                url: "/follow/",
                type: "POST",
                processData: false,
                contentType: false,
                data: form,
                success: function (data) {
                    console.log(data)
                    follow_ajax = false;
                    if (data.status) {
                        // follow
                        button.text("Unfollow")
                    } else {
                        // unfollow
                        button.text("Follow")
                    }
                },
                error: function (xhr, errmsg, err) {

                    console.log(xhr, errmsg, err);

                } // end error: function
            });
        }

    });

});

