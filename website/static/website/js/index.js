$(window).on("load",function(){
	setTimeout(() => {
		$('.loader').css('transform', 'translateY(-100%)');
		$('main').css('display', 'block');
	}, 700);
});