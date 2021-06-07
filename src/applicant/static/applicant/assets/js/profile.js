console.log("Editing Applicant profile")
const editProfileForm = document.getElementById('edit-profile')
const progressBox = document.getElementById('progress-box')
const image = document.getElementById('id_image')
console.log(image)
const error_first_name = document.getElementById('error-first-name')
const error_last_name= document.getElementById('error-last-name')
const error_email = document.getElementById('error-email')
const error_gender = document.getElementById('error-gender')
const error_phone= document.getElementById('error-phone-number')
const error_nationality = document.getElementById('error-nationality')
const error_title = document.getElementById('error-title')
const error_bio = document.getElementById('error-bio')
const csrf = document.getElementsByName("csrfmiddlewaretoken")
const first_name = document.getElementById("id_first_name")
const last_name = document.getElementById("id_last_name")
const email = document.getElementById("id_email")
const nationality = document.getElementById("id_nationality")
const gender = document.getElementById("id_gender")
const phone = document.getElementById("id_phone_number")
const title = document.getElementById("id_title")
const bio = document.getElementById("id_bio")

editProfileForm.addEventListener('submit', (e) => {
    e.preventDefault()
    const image_data = image.files[0]
    console.log(image_data)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('first_name', first_name.value)
    fd.append('last_name', last_name.value)
    fd.append('email', email.value)
    fd.append('nationality', nationality.value)
    fd.append('gender', gender.value)
    fd.append('phone_number', phone.value)
    fd.append('image', image_data)
    fd.append('title', title.value)
    fd.append('bio', bio.value)

    $.ajax({
        type: "POST",
        url: editProfileForm.action,
        enctype: "multipart/form-data",
        data: fd,
        beforeSend: function() {
            $("#error-first-name").html('');
            $("#error-last-name").html('');
            $("#error-email").html('');
            $("#error-phone-number").html('');
            $("#error-gender").html('');
            $("#error-nationality").html('');
            $("#error-image").html('');
            $("#error-title").html('');
            $("#error-bio").html('');
        },
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                //console.log(e)
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    console.log(percent)
                    progressBox.innerHTML = `
                        <div class="progress">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100" style="width: ${percent}%;">
                                <span class="progress-value">${percent.toFixed(1)}%</span>
                            </div>
                        </div>
                        `
                }
            })
            return xhr
        },
        success: function(response) {
            console.log(response)
            if (response.message){
                iziToast.success({
                  title: 'Profile Updated! ',
                  message: response.message,
                  position: 'topRight'
                });
            } else {
            if (response.info){
                iziToast.info({
                  title: 'Profile Not Updated! ',
                  message: response.info,
                  position: 'topRight'
                });
            }
            if (response['form']['first_name']){
            error_first_name.innerHTML = `<p class="text-danger">
            ${response['form']['first_name']}
            </p>`
            }
            if (response['form']['last_name']){
            error_last_name.innerHTML = `<p class="text-danger">
            ${response['form']['last_name']}
            </p>`
            }
            if (response['form']['email']){
            error_email.innerHTML = `<p class="text-danger">
            ${response['form']['email']}
            </p>`
            }
            if (response['p_form']['nationality']){
            error_nationality.innerHTML = `<p class="text-danger">
            ${response['p_form']['nationality']}
            </p>`
            }
            if (response['p_form']['gender']){
            error_gender.innerHTML = `<p class="text-danger">
            ${response['p_form']['gender']}
            </p>`
            }
            if (response['p_form']['phone_number']){
            error_phone.innerHTML = `<p class="text-danger">
            ${response['p_form']['phone_number']}
            </p>`
            }
            if (response['p_form']['title']){
            error_title.innerHTML = `<p class="text-danger">
            ${response['p_form']['title']}
            </p>`
            }
            if (response['p_form']['bio']){
            error_bio.innerHTML = `<p class="text-danger">
            ${response['p_form']['bio']}
            </p>`
            }
            }
        },
        error: function(error) {
            console.log(error)
            iziToast.info({
              title: error.status,
              message: error.statusText,
              position: 'topRight'
            });
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})