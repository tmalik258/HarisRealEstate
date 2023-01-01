$(window).on("load",function(){
	setTimeout(() => {
		$('.loader').css('transform', 'translateY(-100%)');
	}, 500);
	setTimeout(() => {
		$('header').css('display', 'initial');
		$('main').css({opacity: 1, visibility: 'visible'});
	}, 700);
	
	if (window.innerWidth > 990)
	{
		$('.carousel-inner').height(window.innerHeight);
		// $('.top-categories').height(window.innerHeight);
	}
	$('.top-categories .card img').each(item, function (indexInArray, valueOfElement) { 
		console.log(item.height());
	});
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