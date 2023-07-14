// document.onreadystatechange = function (e) {
	// if (document.readyState === 'complete') {
		if (window.innerWidth > 990)
		{
			$('.carousel-inner').height(window.innerHeight - 170);

			
			/* /////////////////////////////////	FADE SCROLL VISUAL	////////////////////////////////// */
			const observer = new IntersectionObserver((entries) => {
				entries.forEach((entry) => {
					// console.log(entry)
					if (entry.isIntersecting)
					{
						entry.target.classList.add('show');
					}
					else
					{
						entry.target.classList.remove('show');
					}
				})
			})

			const hiddenElements = document.querySelectorAll('.hidden');
			hiddenElements.forEach((el) => observer.observe(el));
		}

		 // Toggle for navigation
		 $('.menuToggle').click(() => $('.navigation').toggleClass('active'));
	// }
// }



// window.onload = function(){
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

	let previous_unit = 'M';
	$('#area_size_unit').on('change', function (e) {
		let a_size = $('#area_size').val();
		let current_unit = $('#area_size_unit').val();

		// From Marla to Other Unit Conversions
		if (previous_unit === 'M') {
			if (current_unit === 'K') {
				$('#area_size').val(a_size * 0.05);
			}
			else if (current_unit === 'SFt') {
				$('#area_size').val(a_size * 225);
			}
			else if (current_unit === 'SM') {
				$('#area_size').val(a_size * 20.9);
			}
			else if (current_unit === 'SYd') {
				$('#area_size').val(a_size * 25);
			}
		}

		// From Kanal to Other Unit Conversions
		if (previous_unit === 'K') {
			if (current_unit === 'M') {
				$('#area_size').val(a_size * 20);
			}
			else if (current_unit === 'SFt') {
				$('#area_size').val(a_size * 5445);
			}
			else if (current_unit === 'SM') {
				$('#area_size').val(a_size * 505.857);
			}
			else if (current_unit === 'SYd') {
				$('#area_size').val(a_size * 605.625);
			}
		}
		
		// From SqFt to Other Unit Conversions
		if (previous_unit === 'SFt') {
			if (current_unit === 'K') {
				$('#area_size').val(a_size * 0.0000229568);
			}
			else if (current_unit === 'M') {
				$('#area_size').val(a_size * 0.00367657);
			}
			else if (current_unit === 'SM') {
				$('#area_size').val(a_size * 0.092903);
			}
			else if (current_unit === 'SYd') {
				$('#area_size').val(a_size * 0.111111);
			}
		}
		
		// From SqM to Other Unit Conversions
		if (previous_unit === 'SM') {
			if (current_unit === 'K') {
				$('#area_size').val(a_size * 0.0002517);
			}
			else if (current_unit === 'SFt') {
				$('#area_size').val(a_size * 10.764);
			}
			else if (current_unit === 'M') {
				$('#area_size').val(a_size * 0.027222);
			}
			else if (current_unit === 'SYd') {
				$('#area_size').val(a_size * 1.196);
			}
		}
		
		// From SYd to Other Unit Conversions
		if (previous_unit === 'SYd') {
			if (current_unit === 'K') {
				$('#area_size').val(a_size * 0.0016528926);
			}
			else if (current_unit === 'SFt') {
				$('#area_size').val(a_size * 9);
			}
			else if (current_unit === 'SM') {
				$('#area_size').val(a_size * 0.83612736);
			}
			else if (current_unit === 'M') {
				$('#area_size').val(a_size * 0.0826446281);
			}
		}
		
		previous_unit = current_unit;
	})
	

/* /////////////////////////////////	SWIPER SLIDE SCROLLER	////////////////////////////////// */
	var swiperPopular = new Swiper(".mySwiper", {
		// default parameters
		spaceBetween: 20,
		grapCursor: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
		},
		slidesPerView: 4,
	
		// Responsive breakpoints
		breakpoints: {
			// when window width is less than 990
			0: {
				slidesPerView: 1,
			},

			450: {
				slidesPerView: 2
			},

			990: {
				slidesPerView: 4
			}
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

		navigation: {
		  nextEl: ".swiper-button-next",
		  prevEl: ".swiper-button-prev",
		},
	  });
// };


/* ////////////////////////////////	On Resize for Responsiveness	/////////////////////////////// */
window.onresize = function () {
	if (window.innerWidth < 1400)
	{
		$('.carousel-inner').height("initial");
	}
	else
		$('.carousel-inner').height(window.innerHeight - 170);
			// $('.carousel-inner').height(window.innerHeight );
}


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
		<section class="auth_form">
			<div class="login-body">
				<h1 class="card-text">CONTACT US</h1>
				<p class="text-muted">If you are interested in hearing more about the way we work, have a business proposal, or are interested in making a purchase, we'd love to hear from you.</p>
			</div>
			<form id="contact-us">
				<div class="form-floating">
					<input class="form-control first_name" type="text" placeholder="*First Name" aria-label="First Name" required>
					<label for="floatingInput">What is your First Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control last_name" type="text" placeholder="Last Name" aria-label="Last Name">
					<label for="floatingInput">What is your Last Name?</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control tel_n" pattern="+[0-9]{2}-[0-9]{3}-[0-9]{7}" type="tel" placeholder="*Phone Number" aria-label="Phone Number" required>
					<label for="floatingInput">What is your Phone Number?  (+92-312-3456789)</label>
				</div><br>
				<div class="form-floating">
					<input class="form-control email" type="email" placeholder="*Email" aria-label="Email" required>
					<label for="floatingInput">What is your Email? (name@example.com)</label>
				</div><br>
				<div class="form-floating">
					<textarea class="form-control message" placeholder="Leave a message here" aria-label="Enter Message" id="floatingTextarea2" style="height: 150px" required></textarea>
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

window.onscroll = function () {
	if (window.innerWidth > 990)
	{
		if (window.scrollY >= 90)
		{
			$('.navigation').css('inset', '20px 0 20px 20px');
		}
		else
		{
			$('.navigation').css('inset', '140px 0 20px 20px');
		}
	}
}

function navRemove() {
	var scrollPosition = window.innerHeight + window.scrollY;
	var documentHeight = document.documentElement.scrollHeight;
  
	if (scrollPosition >= documentHeight) {
		$('#navbar-main-menu').hide();
	} else {
		$('#navbar-main-menu').show();
	}
}

if (window.innerWidth < 990)
{
	window.addEventListener('scroll', navRemove);
}