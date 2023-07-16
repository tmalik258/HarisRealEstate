$('.image-gallery .close_btn').click(function (e) { 
	e.preventDefault();
	$('.image-gallery').css('display', 'none');
});

$('.open_gallery').click(function (e) { 
	e.preventDefault();
	$('.image-gallery').css('display', 'flex');
});