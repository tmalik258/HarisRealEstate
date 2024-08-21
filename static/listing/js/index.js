$(function () {
	if (window.innerWidth < 990) {
		window.addEventListener("scroll", navRemove);
	}

	if (window.innerWidth > 990) {
		$(".carousel-inner").height(window.innerHeight - 170);
		if (window.scrollY >= 90) {
			$(".navigation").css("inset", "20px 0 20px 20px");
		} else {
			$(".navigation").css("inset", "200px 0 20px 20px");
		}



		/* /////////////////////////////////	FADE SCROLL VISUAL	////////////////////////////////// */
		const observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					entry.target.classList.add("show");
				} else {
					entry.target.classList.remove("show");
				}
			});
		});

		const hiddenElements = document.querySelectorAll(".hidden");
		hiddenElements.forEach((el) => observer.observe(el));
	}

	// Toggle for navigation
	$(".menuToggle").click(() => $(".navigation").toggleClass("active"));

	if (!$(".contact-us").html()) {
		load_contact_form();
	}

	// To send a message or to save a contact us message
	$("#contact-us").submit(function (e) {
		e.preventDefault();
		return send_message();
	});

	let previous_unit = "M";
	$("#area_size_unit").on("change", function (e) {
		let a_size = $("#area_size").val();
		let current_unit = $("#area_size_unit").val();

		// From Marla to Other Unit Conversions
		if (previous_unit === "M") {
			if (current_unit === "K") {
				$("#area_size").val(a_size * 0.05);
			} else if (current_unit === "SFt") {
				$("#area_size").val(a_size * 225);
			} else if (current_unit === "SM") {
				$("#area_size").val(a_size * 20.9);
			} else if (current_unit === "SYd") {
				$("#area_size").val(a_size * 25);
			}
		}

		// From Kanal to Other Unit Conversions
		if (previous_unit === "K") {
			if (current_unit === "M") {
				$("#area_size").val(a_size * 20);
			} else if (current_unit === "SFt") {
				$("#area_size").val(a_size * 5445);
			} else if (current_unit === "SM") {
				$("#area_size").val(a_size * 505.857);
			} else if (current_unit === "SYd") {
				$("#area_size").val(a_size * 605.625);
			}
		}

		// From SqFt to Other Unit Conversions
		if (previous_unit === "SFt") {
			if (current_unit === "K") {
				$("#area_size").val(a_size * 0.0000229568);
			} else if (current_unit === "M") {
				$("#area_size").val(a_size * 0.00367657);
			} else if (current_unit === "SM") {
				$("#area_size").val(a_size * 0.092903);
			} else if (current_unit === "SYd") {
				$("#area_size").val(a_size * 0.111111);
			}
		}

		// From SqM to Other Unit Conversions
		if (previous_unit === "SM") {
			if (current_unit === "K") {
				$("#area_size").val(a_size * 0.0002517);
			} else if (current_unit === "SFt") {
				$("#area_size").val(a_size * 10.764);
			} else if (current_unit === "M") {
				$("#area_size").val(a_size * 0.027222);
			} else if (current_unit === "SYd") {
				$("#area_size").val(a_size * 1.196);
			}
		}

		// From SYd to Other Unit Conversions
		if (previous_unit === "SYd") {
			if (current_unit === "K") {
				$("#area_size").val(a_size * 0.0016528926);
			} else if (current_unit === "SFt") {
				$("#area_size").val(a_size * 9);
			} else if (current_unit === "SM") {
				$("#area_size").val(a_size * 0.83612736);
			} else if (current_unit === "M") {
				$("#area_size").val(a_size * 0.0826446281);
			}
		}

		previous_unit = current_unit;
	});

	/* /////////////////////////////////	SWIPER SLIDE SCROLLER	////////////////////////////////// */
	var swiperPopular = new Swiper(".propertiesSwiper", {
		// default parameters
		slidesPerView: 1,
		spaceBetween: 20,
		autoplay: {
			delay: 2500,
			disableOnInteraction: false,
		},
		loop: true,

		// Responsive breakpoints
		breakpoints: {
			// when window width is less than 990
			600: {
				slidesPerView: 2,
			},

			992: {
				slidesPerView: 3,
			},

			1200: {
				slidesPerView: 4,
			},

			1400: {
				slidesPerView: 5,
			},
		},
	});
});

/* ////////////////////////////////	On Resize for Responsiveness	/////////////////////////////// */
window.onresize = function () {
	if (window.innerWidth < 990) {
		window.addEventListener("scroll", navRemove);
		$(".navigation").css({"inset": "initial", "bottom": "1.5em", "left": "50%", "transform": "translateX(-50%)"});
	}
	else $(".navigation").css({"inset": "200px 0 20px 20px", "transform": "translateX(0%)"});

	if (window.innerWidth < 1400) {
		$(".carousel-inner").height("initial");
	} else $(".carousel-inner").height(window.innerHeight - 170);
};

/* //////////////////////////////////////	SHOW SCROLL UP	/////////////////////////////////////// */
function scrollUp() {
	const scrollUpBtn = $("#scroll-up");
	$(scrollUpBtn).click(() => {scrollToTop()});
	if (this.scrollY >= 350) {
		scrollUpBtn.addClass("show-scroll");
	} else scrollUpBtn.removeClass("show-scroll");
}
window.addEventListener("scroll", scrollUp);

function scrollToTop() {
	const scrollDuration = 300; // Set the total scroll duration (in milliseconds)
	const start = window.scrollY;
	const startTime = performance.now();

	function scrollStep(timestamp) {
		const currentTime = timestamp - startTime;
		const progress = Math.min(currentTime / scrollDuration, 1); // Calculate progress (0 to 1)
		const easeInOutQuad = progress < 0.5 
			? 2 * progress * progress 
			: -1 + (4 - 2 * progress) * progress; // Ease-in-out function for smoother scrolling
		window.scrollTo(0, start - (start * easeInOutQuad));

		if (progress < 1) {
			requestAnimationFrame(scrollStep);
		}
	}

	requestAnimationFrame(scrollStep);
}

function load_contact_form() {
	$(".contact-us").html(`
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
	`);
}

function send_message() {
	console.log("Send message called");
	fetch("/contact", {
		method: "POST",
		body: JSON.stringify({
			fname: $(".first_name").val(),
			lname: $(".last_name").val(),
			phone_number: $(".tel_n").val(),
			email: $(".email").val(),
			message: $(".message").val(),
		}),
	})
		.then((response) => response.json())
		.then((result) => {
			if (result.message) {
				$("form").remove();
				if (window.innerWidth > 990) {
					$(".contact-us .login-body").css({
						margin: "5%",
						width: "80%",
					});
				} else {
					$(".contact-us .login-body").css({
						margin: "4%",
						width: "80%",
					});
				}
				$(".contact-us .login-body").append(
					`<p class="form_message">${result.message}</p>`
				);
			} else if (result.error) {
				$("#contact-us .form_message").val(`${result.error}`);
			}
			console.log(result);
		});
	return false;
}

window.onscroll = function () {
	if (window.innerWidth > 990) {
		if (window.scrollY >= 90) {
			$(".navigation").css("inset", "20px 0 20px 20px");
		} else {
			$(".navigation").css("inset", "200px 0 20px 20px");
		}
	}
};

function navRemove() {
	var scrollPosition = window.innerHeight + window.scrollY;
	var documentHeight = document.documentElement.scrollHeight;

	if (scrollPosition >= documentHeight) {
		$("#navbar-main-menu").hide();
	} else {
		$("#navbar-main-menu").show();
	}
}
