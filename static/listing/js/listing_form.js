$(document).ready(function () {
	 // When a tab is shown
	 $('.nav-link').on('shown.bs.tab', function (e) {
		// Get the value of the selected radio button in the corresponding tab pane
		var category = $(e.target.getAttribute('data-bs-target')).attr('aria-labelledby');
		switch(category) {
			case 'home-tab':
				// Furnished and Construction State
				$('#furnished_state').css('display', 'flex');
				$('#furnished_state #furnished_field input#furnished_option1').prop('checked', true);
				$('#furnished_state #state_field input#construction-state-option1').prop('checked', true);

				// Bedrooms and Bathrooms
				$('#beds_baths').css('display', 'flex');
				$('#beds_baths #bedroom_field input#bedroom_option0').prop('checked', true);

				// Floor
				$('#floor_col').css('display', 'none');
				$('#floor_col #floor_field input[name="floor"]').each(function (_index, element) {
					// element == this
					$(element).prop('checked', false);
				});
				$('#id_custom_floor').val('');

				// Amenities
				InputUncheck();
				$('#amentity_label').css('display', 'block');
				$('.amenities_plot').css('display', 'none');
				$('.amenities_commercial').css('display', 'none');
				$('.amenities_home').css('display', 'inline');
				break;
			case 'plot-tab':
				// Furnished and Construction State
				$('#furnished_state').css('display', 'none');
				$('#furnished_state input').each(function (_index, element) {
					// element == this
					$(element).prop('checked', false);
				});

				// Bedrooms and Bathrooms
				$('#beds_baths').css('display', 'none');
				$('#beds_baths input').each(function (_index, element) {
					// element == this
					$(element).prop('checked', false);
				});
				$('#id_custom_bedroom').val('');
				$('#id_custom_bathroom').val('');

				// Floor
				$('#floor_col').css('display', 'none');
				$('#floor_col #floor_field input[name="floor"]').each(function (index, element) {
					// element == this
					$(element).prop('checked', false);
				});
				$('#id_custom_floor').val('');

				// Amenities
				InputUncheck();
				$('#amentity_label').css('display', 'block');
				$('.amenities_home').css('display', 'none');
				$('.amenities_commercial').css('display', 'none');
				$('.amenities_plot').css('display', 'inline');
				break;
			case 'commercial-tab':
				// Furnished and Construction State
				$('#furnished_state').css('display', 'flex');
				$('#furnished_state #furnished_field input#furnished_option1').prop('checked', true);
				$('#furnished_state #state_field input#construction-state-option1').prop('checked', true);

				// Bedrooms and Bathrooms
				$('#beds_baths').css('display', 'none');
				$('#beds_baths input').each(function (_index, element) {
					// element == this
					$(element).prop('checked', false);
				});
				$('#id_custom_bedroom').val('');
				$('#id_custom_bathroom').val('');

				// Floor
				$('#floor_col').css('display', 'block');

				// Amenities
				InputUncheck();
				$('#amentity_label').css('display', 'block');
				$('.amenities_home').css('display', 'none');
				$('.amenities_plot').css('display', 'none');
				$('.amenities_commercial').css('display', 'inline');
				break;
			case 'room-tab':
				// Furnished and Construction State
				$('#furnished_state').css('display', 'none');
				$('#furnished_state input').each(function (index, element) {
					// element == this
					$(element).prop('checked', false);
				});

				// Bedrooms and Bathrooms
				$('#beds_baths').css('display', 'none');
				$('#beds_baths input').each(function (_index, element) {
					// element == this
					$(element).prop('checked', false);
				});
				$('#id_custom_bedroom').val('');
				$('#id_custom_bathroom').val('');

				// Floor
				$('#floor_col').css('display', 'block');

				// Amenities
				InputUncheck();
				$('#amentity_label').css('display', 'none');
				$('.amenities_home').css('display', 'none');
				$('.amenities_plot').css('display', 'none');
				$('.amenities_commercial').css('display', 'none');
				break;
			case 'other-tab':
				// Furnished and Construction State
				$('#furnished_state').css('display', 'flex');
				$('#furnished_state #furnished_field input#furnished_option1').prop('checked', true);
				$('#furnished_state #state_field input#construction-state-option1').prop('checked', true);

				// Bedrooms and Bathrooms
				$('#beds_baths').css('display', 'flex');
				$('#beds_baths #bedroom_field input#bedroom_option0').prop('checked', true);

				// Floor
				$('#floor_col').css('display', 'block');

				// Amenities
				InputUncheck();
				$('#amentity_label').css('display', 'block');
				$('.amenities_home').css('display', 'inline');
				$('.amenities_plot').css('display', 'inline');
				$('.amenities_commercial').css('display', 'inline');
				break;
		}
	  });

	// Floor field input
	$('#floor_field input[name="floor"]').on('change', () => {
		let input_val = $(`#floor_field input[name="floor"]:checked`).val();
		$('#id_custom_floor').val(input_val);
		if (input_val === '10') {
			$('#id_custom_floor').css('display', 'block');
		}
		else
			$('#id_custom_floor').css('display', 'none');
	});

	// Bedroom field input
	$('#id_custom_bedroom').val("Studio");
	$('#bedroom_field input[name="bedroom"]').on('change', () => {
		let input_val = $('#bedroom_field input[name="bedroom"]:checked').val();
		$('#id_custom_bedroom').val(input_val);
		if (input_val === '10') {
			$('#id_custom_bedroom').css('display', 'block');
		}
		else
			$('#id_custom_bedroom').css('display', 'none');
	});

	// Bathroom field input
	$('#bathroom_field input[name="bathroom"]').on('change', () => {
		let input_val = $(`#bathroom_field input[name="bathroom"]:checked`).val();
		$('#id_custom_bathroom').val(input_val);
		if (input_val === '8') {
			$('#id_custom_bathroom').css('display', 'block');
		}
		else
			$('#id_custom_bathroom').css('display', 'none');
	});

	// Price Field input
	$('#id_price').on('input', function (e) {
		let val = $('#id_price').val();
		if (val >= 1000000000) {
			$('#id_price_in_words').text((val/1000000000).toFixed(2) + " arab");
		}
		else if (val >= 10000000) {
			$('#id_price_in_words').text((val/10000000).toFixed(2) + " crore");
		}
		else if (val >= 100000) {
				$('#id_price_in_words').text((val/100000).toFixed(2) + " lakh");
		}
		else if (val >= 10000)
		{
			$('#id_price_in_words').text((val/1000).toFixed(2) + " thousand");
		}
		else if (val < 10000)
		{
			$('#id_price_in_words').text("");
		}
	});

	// Form Submit
	$('form').submit(function (e) { 
		// e.preventDefault();

		// Purpose Field
		$('#id_purpose').val($('#purpose_field input[name="purpose"]:checked').val())

		// Furnished Field
		$('#id_furnished').val($('#furnished_field input[name="furnished"]:checked').val())

		// Construction State Field
		$('#id_state').val($('#state_field input[name="construction-state"]:checked').val())

		Category();

		if(!$("#id_images").val()) {
			$('#image_error').text('Images are required (note: other fields may have been reset)');
			return false;
		}
		
		// e.preventDefault();
	});
});

function Category () {
	let tab_pane = $('#myTabContent .tab-pane.show.active');
	let label_pane = $(tab_pane).attr('aria-labelledby');
	let input_val;
	switch(label_pane) {
		case 'home-tab':
		case 'plot-tab':
		case 'commercial-tab':
			let input = $(tab_pane).find(`input[name="${label_pane}-pane"]:checked`);
			input_val = $(input).val();
			break;
		case 'room-tab':
			input_val = 'Room'
			break;
		case 'other-tab':
			input_val = 'Other'
			break;
	}
	console.log('hello')
	var categoryDropdown = document.getElementById("id_category");
	var options = categoryDropdown.options;

	for (var option of options) {
		if (option.text.includes(input_val)) {
			option.selected = true;
			break;
		}
	}
}

function InputUncheck () {
	$('#amenities input[name="amenities"]').each(function (_index, element) {
		// element == this
		$(element).prop('checked', false);
	});
}