// AJAX for posting
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function RightAnswer(id, type) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/rightAnswer/',
        type: 'POST',
        data: {id: id, type: type},
        success: function (data) {
            if (data.errors == "") {

                if (data.makeit == false) {
                    var lable = document.getElementById('A' + id + '+');
                    var button = document.getElementById('A' + id + '+' + 'b');
                    var lable1 = document.getElementById('A' + id + '-');
                    var button1 = document.getElementById('A' + id + '-' + 'b');
                    lable.textContent = "You have already set it as right answer";
                    button.textContent = "Wrong answer!";
                    button.class = "btn-danger";
                    button.className = "btn-outline-danger";
                    lable1.textContent = "You have already set it as right answer";
                    button1.textContent = "Wrong answer!";
                    button1.class = "btn-danger";
                    button1.className = "btn-outline-danger";
                } else {

                    var lable = document.getElementById('A' + id + '+');
                    var button = document.getElementById('A' + id + '+' + 'b');
                    var lable1 = document.getElementById('A' + id + '-');
                    var button1 = document.getElementById('A' + id + '-' + 'b');
                    lable.textContent = "";
                    button.textContent = "Right answer!";
                    button.class = "btn-danger";
                    button.className = "btn-success";
                    lable1.textContent = "";
                    button1.textContent = "Right answer!";
                    button1.class = "btn-danger";
                    button1.className = "btn-success";
                }
            } else if (data.errors == "ANONYMOUS_USER") {
                alert('Only authorized users can do that, please sign in or sign up');
            }
        },
        failure: function (data) {
            alert('error')
        }
    })
}
