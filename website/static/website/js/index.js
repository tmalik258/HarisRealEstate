$(window).on("load",function(){
	$('.loader').css('transform', 'translateY(-100%)');
	$('header').css('display', 'initial');
	$('main').css({opacity: 1, visibility: 'visible'});
	
	if (window.innerWidth > 990)
	{
		$('.carousel-inner').height(window.innerHeight);
		// $('.top-categories').height(window.innerHeight);
	}

	// To send a message or to save a contact us message
	$('#contact-us').submit(function () { 
		return send_message();
	  });
});

function send_message() {
	fetch('/contact_message', {
	  method: 'POST',
	  body: JSON.stringify({
		fname: $('#first_name').val(),
		lname: $('#last_name').val(),
		email: $('#email').val(),
		message: $('#message').val()
	  })
	})
	.then(response => response.json())
	.then(result => {
		if(result.message){
			$('form').remove();
			$('.contact-us .login-body').css('margin', '5%');
			$('.contact-us .login-body').append(`<p class="form_message">${result.message}</p>`);
		}
		else if (result.error)
		{
			$('.contact-us .login-body').append(`<p class="form_message">${result.error}</p>`);
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