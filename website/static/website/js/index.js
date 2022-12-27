$(window).on("load",function(){
	setTimeout(() => {
		$('.loader').css('transform', 'translateY(-100%)');
		$('header').css('display', 'initial');
		$('main').css('display', 'block');
	}, 700);

});