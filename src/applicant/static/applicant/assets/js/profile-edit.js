$(document).ready(function() {
        $("#edit-profile").submit(function(event) {
           event.preventDefault();
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    enctype: "multipart/form-data",
                    async: false,
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
                    success: function(response) {
                         console.log(response);
                         if(response['message']) {
                             iziToast.success({
                              title: 'Profile Updated! ',
                              message: response['message'],
                              position: 'topRight'
                            });
                         }
                         if(response['info']) {
                             iziToast.info({
                              title: 'Info',
                              message: response['info'],
                              position: 'topRight'
                            });
                         }
                         if(response['p_form']) {
                           if(response['p_form']['first_name']) {
                               $("#error-first-name").html(response['p_form']['first_name']);
                           }
                           if(response['p_form']['last_name']) {
                               $("#error-last-name").html(response['p_form']['last_name']);
                           }
                           if(response['p_form']['email']) {
                               $("#error-email").html(response['p_form']['email']);
                           }
                           if(response['p_form']['phone_number']) {
                               $("#error-phone-number").html(response['p_form']['phone_number']);
                           }
                           if(response['p_form']['gender']) {
                               $("#error-gender").html(response['p_form']['gender']);
                           }
                           if(response['p_form']['nationality']) {
                               $("#error-nationality").html(response['p_form']['nationality']);
                           }
                           if(response['p_form']['image']) {
                               $("#error-imager").html(response['p_form']['image']);
                           }
                         }
                         if(response['error']) {
                             $("#message").html("<div class='alert alert-danger'>" +
                                   response['error']['comment'] +"</div>");
                         }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
       });
    })