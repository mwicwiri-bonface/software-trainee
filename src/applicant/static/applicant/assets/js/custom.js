
console.log("Apply Job JS.")
var applyBtns = document.getElementsByClassName('apply-btn')
function stop_reloading(slug) {
  $('#'+slug).removeClass('disabled btn-progress');
}
for (i = 0; i < applyBtns.length; i++) {
	applyBtns[i].addEventListener('click', function(){
		var slug = this.dataset.slug
		console.log('Slug:', slug)
        applyJob(slug)
        console.log(this)
        this.className += "disabled btn-progress";
	})
}

function applyJob(slug){
	    console.log('applying job.')
		var url = apply_job_url

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'slug':slug})
		})
		.then((response) => {
		    console.log(response)
		    stop_reloading(slug);
		    if (response['statusText'] != 'OK'){
		    iziToast.error({
              title: response['status'],
              message: response['statusText'],
              position: 'topRight'
            });
            }
		   return response.json();
		})
		.then((data) => {
		    console.log(data)
		    if (data['message']){
                iziToast.success({
                  title: 'Job Applied! ',
                  message: data['message'],
                  position: 'topRight'
                });
		    } else if (data['info']){
                iziToast.info({
                  title: 'Info!',
                  message: data['info'],
                  position: 'topRight'
                });
		    }
		});
}