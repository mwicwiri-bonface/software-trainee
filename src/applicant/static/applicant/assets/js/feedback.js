console.log("Feedback")
$(document).ready(function() {
        $("#feedback").submit(function(event) {
           event.preventDefault();
           $('#feedback-btn').addClass('disabled btn-progress');
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    enctype: "multipart/form-data",
                    beforeSend: function() {
                        $("#error-subject").html('');
                        $("#error-message").html('');
                    },
                    success: function(response) {
                         console.log(response);
                         $('#feedback-btn').removeClass('disabled btn-progress');
                         if(response['message']) {
                             iziToast.success({
                              title: 'Feedback Sent! ',
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
                         if(response['form']) {
                           if(response['form']['subject']) {
                               $("#error-subject").html(response['form']['subject']);
                           }
                           if(response['form']['message']) {
                               $("#error-message").html(response['form']['message']);
                           }
                         }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                         if(error == "Forbidden"){
                         iziToast.error({
                              title: 403,
                              message: error,
                              position: 'topRight'
                            });
                         location.reload()
                         }
                         else{
                         iziToast.error({
                              title: status,
                              message: error,
                              position: 'topRight'
                            });
                         }
                    }
           });
       });
    })