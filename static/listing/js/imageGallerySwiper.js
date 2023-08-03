var swiper = new Swiper(".imagesGallerySwiper", {
	lazy: true,
	zoom: true,
	spaceBetween: 10,
	pagination: {
	  el: ".swiper-pagination",
	  clickable: true,
	},
	navigation: {
	  nextEl: ".swiper-button-next",
	  prevEl: ".swiper-button-prev",
	},
});