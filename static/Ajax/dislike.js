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


function Dislike(id, type) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/dislike/',
        type: 'POST',
        data: {id: id, type: type},
        success: function (data) {
            if (data.errors == "") {
                var doc = document.getElementById(type + id);
                doc.textContent = data.likes + ' рейтинг';
            } else if (data.errors == "ALREADY_DISLIKED"){
                alert('You have already disliked this, please stop doing that!')
            } else if(data.errors=="ANONYMOUS_USER"){
                alert('Only authorized users can do that, please sign in or sign up');
            }
         },
        failure: function (data) {
            alert('error')
        }
    })
}