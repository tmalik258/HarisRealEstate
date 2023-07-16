const accordion = $('.accordion');

$(accordion).click(function (e) { 
	// e.preventDefault();
	const activePanel = e.target.closest('.accordion-panel');
	if (!activePanel) return;

	toggleAccordion(activePanel);
});

function toggleAccordion(panelToActive) {
	const btns = panelToActive.parentElement.querySelectorAll("button");
	const contents = panelToActive.parentElement.querySelectorAll(".accordion-content");
	btns.forEach((btn) => {
		btn.setAttribute("aria-expanded", false);
	});
	contents.forEach((content) => {
		content.setAttribute("aria-hidden", true);
	});
	panelToActive.querySelector("button").setAttribute("aria-expanded", true);
	panelToActive.querySelector(".accordion-content").setAttribute("aria-hidden", false);
}

$(document).ready(function () {
	let expanded = false;
	$('.accordion button').each(function () {
	  if ($(this).attr('aria-expanded') === 'true') {
		expanded = true;
		return false; // Exit the loop if any button has aria-expanded set to true
	  }
	});
	if (!expanded) {
		$('.accordion button').eq(0).attr('aria-expanded', true);
	}
	else {
		if (window.innerWidth < 990) {
			const activePanel = document.querySelector('.accordion-panel:first-child');
			toggleAccordion(activePanel);
		}
	}
});