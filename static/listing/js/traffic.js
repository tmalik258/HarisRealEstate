function countAnimation(id, total) {
	var id_traffic_count = document.getElementById(id);
	var count = 0;
  
	var interval = setInterval(function() {
		id_traffic_count.textContent = count;
		count++;
	
		if (count > 100) {
			clearInterval(interval);
		}
	}, 10);
}

window.onscroll = function () {
	if($('#counter_section').hasClass('show'))
	{
		countAnimation('traffic_count', TRAFFIC_COUNT);
		countAnimation('sale_count', SALE_COUNT);
		countAnimation('rent_count', RENT_COUNT);
	}
}
countAnimation('traffic_count', TRAFFIC_COUNT);
countAnimation('sale_count', SALE_COUNT);
countAnimation('rent_count', RENT_COUNT);
