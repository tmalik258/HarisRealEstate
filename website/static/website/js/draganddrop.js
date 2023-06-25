// Add event listeners for drag and drop functionality
var dropzone = document.getElementById('dropzone');

// Get the file input element and the image preview container
var fileInput = document.getElementById('listing-image');
var imagePreview = document.getElementById('image-preview');

dropzone.addEventListener('dragenter', handleDragEnter, false);
dropzone.addEventListener('dragover', handleDragOver, false);
dropzone.addEventListener('dragleave', handleDragLeave, false);
dropzone.addEventListener('drop', handleDrop, false);

function handleDragEnter(e) {
  e.preventDefault();
  e.stopPropagation();
  // Add any visual effects when the dragged element enters the dropzone
  dropzone.classList.add('drag-over');
}

function handleDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  // Add any visual effects when the dragged element is over the dropzone
  dropzone.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.preventDefault();
  e.stopPropagation();
  // Remove any visual effects when the dragged element leaves the dropzone
  dropzone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    // Remove any visual effects when the dragged element is dropped
    // dropzone.classList.remove('drag-over');
    // Handle the dropped files
    var files = e.dataTransfer.files;
	// Clear the image preview container
	imagePreview.innerHTML = '';
    // Process the files as per your requirements, such as saving them to the database or storing them on the server
    for (var i = 0; i < files.length; i++) {
		var file = files[i];
    createImagePreview(file);
    }
	dropzone.classList.remove('drag-over');
  }


// Add an event listener to the file input element
fileInput.addEventListener('change', function() {
  // Clear the image preview container
  imagePreview.innerHTML = '';

  // Get the selected files
  var files = fileInput.files;

  // Iterate over the selected files
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    createImagePreview(file);
  }
});

function createImagePreview(file) {
  var reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function(e) {
    var image = document.createElement('img');
    image.classList.add('image-preview');
    image.src = e.target.result;

    var deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button', 'btn', 'btn-sm', 'btn-danger', 'mx-auto', 'mt-2');
    deleteButton.textContent = 'Remove';
    deleteButton.addEventListener('click', function() {
      var inputFile = document.getElementById('listing-image');
      var imageFile = inputFile.files[Array.from(imagePreview.children).indexOf(previewContainer)];
      var dt = new DataTransfer();
      Array.from(inputFile.files).forEach(function (file) {
        if (file !== imageFile) {
          dt.items.add(file);
        }
      });
      inputFile.files = dt.files;
      imagePreview.removeChild(previewContainer);
    });

    var previewContainer = document.createElement('div');
    previewContainer.classList.add('image-preview-container');
    previewContainer.appendChild(image);
    previewContainer.appendChild(deleteButton);

    imagePreview.appendChild(previewContainer);
  };
}
