// To use Ajax and jQuery in a more secure way we add csrftoken for these frameworks

function getCookie(name){
    var CookieValue = null;
    if (document.cookie &&  document.cookie !== ''){
        var cookies = document.cookie.split(';')
        for (i=0; i<cookies.length; i++){
            var cookie= jQuery.trim((cookies[i]))
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) ===    (name + '=')){
                CookieValue = decodeURIComponent(cookie.substring(name.length +1));
                break;
            }
        }
    }
        return CookieValue
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method){
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

}
$.ajaxSetup({
    beforeSend: function(xhr,settings){
        if(!csrfSafeMethod(settings.type) && !this.CrossDomain){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
})