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