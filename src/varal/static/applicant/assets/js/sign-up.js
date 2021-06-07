console.log("creating Applicant account")
const signUpForm = document.getElementById('applicant-sign-up-form')
const alertBox = document.getElementById('alert-box')
const error_first_name = document.getElementById('error-first-name')
const error_last_name= document.getElementById('error-last-name')
const error_email = document.getElementById('error-email')
const error_password1 = document.getElementById('error-password1')
const error_password2 = document.getElementById('error-password2')
const csrf = document.getElementsByName("csrfmiddlewaretoken")
const first_name = document.getElementById("id_first_name")
const last_name = document.getElementById("id_last_name")
const email = document.getElementById("id_email")
const password1 = document.getElementById("id_password1")
const password2 = document.getElementById("id_password2")
signUpForm.addEventListener('submit', (e) => {
    e.preventDefault()
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('first_name', first_name.value)
    fd.append('last_name', last_name.value)
    fd.append('email', email.value)
    fd.append('password1', password1.value)
    fd.append('password2', password2.value)

    $.ajax({
        type: "POST",
        url: signUpForm.action,
        enctype: "multipart/form-data",
        data: fd,
        beforeSend: function() {
            console.log('before')
            alertBox.innerHTML = ""
            error_first_name.innerHTML = ""
            error_last_name.innerHTML = ""
            error_email.innerHTML = ""
            error_password1.innerHTML = ""
            error_password2.innerHTML = ""
        },
        success: function(response) {
            console.log(response)
            if (response.message){
            iziToast.success({
                    title: '',
                    message: response.message,
                    position: 'topRight'
                  });
            }else{
            if (response.first_name){
            error_first_name.innerHTML = `<p class="text-danger">
            ${response.first_name}
            </p>`
            }
            if (response.last_name){
            error_last_name.innerHTML = `<p class="text-danger">
            ${response.last_name}
            </p>`
            }
            if (response.email){
            error_email.innerHTML = `<p class="text-danger">
            ${response.email}
            </p>`
            }
            if (response.password1){
            error_password1.innerHTML = `<p class="text-danger">
            ${response.password1}
            </p>`
            }
            if (response.password2){
            error_password2.innerHTML = `<p class="text-danger">
            ${response.password2}
            </p>`
            }
            }
        },
        error: function(error) {
            iziToast.error({
            title: error.status,
            message: error.statusText,
            position: 'topRight'
            });
            $(window).scrollTop(0);
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})