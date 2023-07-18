$(document).ready(function () {
	// floor field input
	$('#floor_field input[name="floor"]').on('change', () => {
		let input_val = $(`#floor_field input[name="floor"]:checked`).val();
		$('#id_custom_floor').val(input_val);
		if (input_val === '10') {
			$('#id_custom_floor').css('display', 'block');
		}
		else
			$('#id_custom_floor').css('display', 'none');
	});

	// bedroom field input
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

	$('form').submit(function (e) { 
		// e.preventDefault();

		// Purpose Field
		$('#id_purpose').val($('#purpose_field input[name="purpose"]:checked').val())

		// Furnished Field
		$('#id_furnished').val($('#furnished_field input[name="furnished"]:checked').val())

		// Construction State Field
		$('#id_state').val($('#state_field input[name="construction-state"]:checked').val())

		Category();

		var fileInput = document.getElementById('id_images');

		if (fileInput.files.length === 0) {
			e.preventDefault(); // Prevent the form from submitting
			alert('Please select at least one image.'); // Display an error message
		  }
		  else {
			console.log(fileInput.files.length)
		  }
		// return false;
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

	var categoryDropdown = document.getElementById("id_category");
	var options = categoryDropdown.options;

	for (var option of options) {
		if (option.text.includes(input_val)) {
			option.selected = true;
			break;
		}
	}
}