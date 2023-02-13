document.onreadystatechange = function (e) {
	if (document.readyState === 'complete') {
		$('.loader').css('transform', 'translateY(-100%)');
		$('header').css('display', 'initial');
		$('main').css({display: 'block'});
		$('footer').css({display: 'block'});
		
		if (window.innerWidth > 990)
		{
			$('.carousel-inner').height(window.innerHeight);
			// $('.top-categories').height(window.innerHeight);
		}
	}
}

window.onload = function(){
	//	load contact form virtually
	if (!$('.contact-us').html()) {
		load_contact_form();
	}
	
	
	// To send a message or to save a contact us message
	$('#contact-us').submit(function (e) { 
		e.preventDefault();
		return send_message();
	});
};

function load_contact_form () {
	$('.contact-us').html(`
		<section class="login">
			<div class="login-body">
				<h1 class="card-text">CONTACT US</h1>
				<p class="text-muted">If you are interested in hearing more about the way we work, have a business proposal, or are interested in making a purchase, we'd love to hear from you.</p>
			</div>
			<form id="contact-us">
				<div class="form-floating">
					<input class="form-control first_name" type="text" id="floatingInput" placeholder="*First Name" required>
					<label for="floatingInput">What is your First Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control last_name" type="text" id="floatingInput" placeholder="Last Name">
					<label for="floatingInput">What is your Last Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control email" type="email" id="floatingInput" placeholder="*Email" required>
					<label for="floatingInput">What is your Email? (name@example.com)</label>
				</div><br>
				<div class="form-floating">
					<textarea class="form-control message" placeholder="Leave a message here" id="floatingTextarea2" style="height: 150px" required></textarea>
					<label for="floatingTextarea2">What is your Message?</label>
				</div>
				<p class="form_message"></p>
				<input type="submit" class="btn btn-dark" value="SEND">
			</form>
		</section>
	`)
}

function send_message() {
	console.log("Send message called");
	fetch('/contact', {
	  method: 'POST',
	  body: JSON.stringify({
		fname: $('.first_name').val(),
		lname: $('.last_name').val(),
		email: $('.email').val(),
		message: $('.message').val()
	  })
	})
	.then(response => response.json())
	.then(result => {
		if(result.message){
			$('form').remove();
			if (window.innerWidth > 990)
			{
				$('.contact-us .login-body').css({
					'margin': '5%',
					'width': '80%'
				});
			}
			else
			{
				$('.contact-us .login-body').css({
					'margin': '4%',
					'width': '80%'
				});
			}
			$('.contact-us .login-body').append(`<p class="form_message">${result.message}</p>`);
		}
		else if (result.error)
		{
			$('#contact-us .form_message').val(`${result.error}`);
		}
		console.log(result);
	})
	return false;
}

window.onscroll = function () {
	if (window.scrollY >= 50)
	{
		$('.navbar').addClass('active');
		hideHeader();
	}
	else
	{
		$('.navbar').removeClass('active');
	}
}

let lastScrollPos = 0;

const hideHeader = function () {
	const isScrollButton = lastScrollPos < window.scrollY;
	if (isScrollButton){
		$('.navbar').addClass('hide');
		// $('.navbar').width('100%');
	}
	else
		$('.navbar').removeClass('hide');

	lastScrollPos = window.scrollY;
}