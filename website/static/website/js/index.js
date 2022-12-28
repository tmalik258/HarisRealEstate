$(window).on("load",function(){
	setTimeout(() => {
		$('.loader').css('transform', 'translateY(-100%)');
		$('header').css('display', 'initial');
		$('main').css('display', 'block');
	}, 700);
	
	if (window.innerWidth > 990)
	{
		$('.carousel-inner').height(window.innerHeight);
		$('.top-categories').height(window.innerHeight);
	}
});

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