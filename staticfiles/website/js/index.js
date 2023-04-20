document.onreadystatechange = function (e) {
	if (document.readyState === 'complete') {
		if (window.innerWidth > 990)
		{
			$('.carousel-inner').height(window.innerHeight);
		}
	}
}

window.onresize = function () {
	if (window.innerWidth < 990)
	{
		$('.carousel-inner').height("initial");
	}
	else
		$('.carousel-inner').height(window.innerHeight);
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


	// To make create listing form dynamic
	const category_list = ['house', 'flat', 'up', 'lp', 'fh', 'room', 'ph']
	$('#category_input').on('change', function (e) {
		if(!category_list.includes($('#category_input').val())){
			$('#bedroom').hide();
			$('#bathroom').hide();
		}
		else
		{
			$('#bedroom').show();
			$('#bathroom').show();
		}
	})

	$('#price_input').on('input', function (e) {
		let val = $('#price_input').val();
		if (val >= 1000000000) {
			$('#price_int_word').text(($('#price_input').val()/1000000000).toFixed(2) + " arab");
		}
		else if (val >= 10000000) {
			$('#price_int_word').text(($('#price_input').val()/10000000).toFixed(2) + " crore");
		}
		else if (val >= 100000) {
				$('#price_int_word').text(($('#price_input').val()/100000).toFixed(2) + " lakh");
		}
		else if (val >= 10000)
		{
			$('#price_int_word').text(($('#price_input').val()/1000).toFixed(2) + " thousand");
		}
		else if (val < 10000)
		{
			$('#price_int_word').text("");
		}
	});
	
	
	// SWIPER SLIDE SCROLLER
	var swiperPopular = new Swiper(".mySwiper", {
		// default parameters
		spaceBetween: 20,
		grapCursor: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
		},
		slidesPerView: 1,
	
		// Responsive breakpoints
		breakpoints: {
			// when window width is less than 990
			450: {
				slidesPerView: 2
			},

			990: {
				slidesPerView: 4
			}
		},

		scrollbar: {
			el: ".swiper-scrollbar",
		},
		
		navigation: {
		  nextEl: ".swiper-button-next",
		  prevEl: ".swiper-button-prev",
		},
	});

	var swiperImages = new Swiper(".singlePropertyImageSwiper", {
		effect: "coverflow",
		grabCursor: true,
		centeredSlides: true,
		slidesPerView: "auto",
		coverflowEffect: {
			rotate: 50,
			stretch: 0,
			depth: 100,
			modifier: 1,
			slideShadows: true,
		},
		
		pagination: {
			el: ".swiper-pagination",
		},

		scrollbar: {
			el: ".swiper-scrollbar",
		},
		
		navigation: {
		  nextEl: ".swiper-button-next",
		  prevEl: ".swiper-button-prev",
		},
	  });



	};
	
/* //////////////////////////////////////	SHOW SCROLL UP	/////////////////////////////////////// */
function scrollUp() {
	const scrollUp = $('#scroll-up');
	if (this.scrollY >= 350) {
		scrollUp.addClass('show-scroll');
	}
	else
		scrollUp.removeClass('show-scroll');
}
window.addEventListener('scroll', scrollUp)

function load_contact_form () {
	$('.contact-us').html(`
		<section class="login">
			<div class="login-body">
				<h1 class="card-text">CONTACT US</h1>
				<p class="text-muted">If you are interested in hearing more about the way we work, have a business proposal, or are interested in making a purchase, we'd love to hear from you.</p>
			</div>
			<form id="contact-us">
				<div class="form-floating">
					<input class="form-control first_name" type="text" id="floatingInput" placeholder="*First Name" aria-id=1 required>
					<label for="floatingInput">What is your First Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control last_name" type="text" id="floatingInput" placeholder="Last Name" aria-id=2>
					<label for="floatingInput">What is your Last Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control tel_n" pattern="+[0-9]{2}-[0-9]{3}-[0-9]{7}" type="tel" id="floatingInput" placeholder="*Phone Number" aria-id=3 required>
					<label for="floatingInput">What is your Phone Number?  (+92-312-3456789)</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control email" type="email" id="floatingInput" placeholder="*Email" aria-id=4 required>
					<label for="floatingInput">What is your Email? (name@example.com)</label>
				</div><br>
				<div class="form-floating">
					<textarea class="form-control message" placeholder="Leave a message here" aria-id=5 id="floatingTextarea2" style="height: 150px" required></textarea>
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
		phone_number: $('.tel_n').val(),
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

// window.onscroll = function () {
// 	if (window.scrollY >= 50)
// 	{
// 		$('.navbar').addClass('active');
// 		hideHeader();
// 	}
// 	else
// 	{
// 		$('.navbar').removeClass('active');
// 	}
// }

// let lastScrollPos = 0;

// const hideHeader = function () {
// 	const isScrollButton = lastScrollPos < window.scrollY;
// 	if (isScrollButton){
// 		$('.navbar').addClass('hide');
// 		// $('.navbar').width('100%');
// 	}
// 	else
// 		$('.navbar').removeClass('hide');

// 	lastScrollPos = window.scrollY;
// }