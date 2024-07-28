// Add event listeners for drag and drop functionality
var dropzone = document.getElementById('dropzone');

// Get the file input element and the image preview container
var fileInput = document.getElementById('id_images');
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
  dropzone.classList.remove('drag-over');
  // Handle the dropped files
  // Clear the image preview container
  imagePreview.innerHTML = '';

  // Get the selected files
  for (const file in e.dataTransfer.files) {
    if (Object.hasOwnProperty.call(e.dataTransfer.files, file)) {
      const element = e.dataTransfer.files[file];
      selectedImages.push([element, element.name]);
    }
  }
  var dt = new DataTransfer();
  selectedImages.forEach(img => {
    var blob = new Blob([img[0]], {type: 'image/*'})
    dt.items.add(new File([blob], img[1]));
  });
  var files = fileInput.files = dt.files;

  // Process the files as per your requirements, such as saving them to the database or storing them on the server
  for (var i = 0; i < files.length; i++) {
    createImagePreview(files[i], fileInput);
  }
}

  // Add an event listener to the file input element
fileInput.addEventListener('change', function() {
  // Clear the image preview container
  imagePreview.innerHTML = '';

  // Get the selected files
  for (const file in fileInput.files) {
    if (Object.hasOwnProperty.call(fileInput.files, file)) {
      const element = fileInput.files[file];
      selectedImages.push([element, element.name]);
    }
  }
  var dt = new DataTransfer();
  selectedImages.forEach(img => {
    var blob = new Blob([img[0]], {type: 'image/*'})
    dt.items.add(new File([blob], img[1]));
  });
  var files = fileInput.files = dt.files;

  // Iterate over the selected files
  for (var i = 0; i < files.length; i++) {
    createImagePreview(files[i], fileInput);
  }
});

function createImagePreview(file, inputFile) {
  var reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function(e) {
    var image = document.createElement('img');
    image.classList.add('image-preview');
    image.src = e.target.result;
    image.alt = 'image_' + e.target.result;
  
    // selectedImages.push(e.target.result);

    var deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button', 'btn', 'btn-sm', 'mx-auto', 'mt-2');
    deleteButton.textContent = 'Remove';
    deleteButton.addEventListener('click', function (e) {
      e.preventDefault();
      var imageFile = inputFile.files[Array.from(imagePreview.children).indexOf(previewContainer)];
      imageFile = imageFile.name;
      //  Remove the image from the selectedImages array
      var dt = new DataTransfer();

      selectedImages = selectedImages.filter(function (img) {
        if (img[1] !== imageFile) {
          var blob = new Blob([img[0]], {type: 'image/*'})
          dt.items.add(new File([blob], img[1]));
          return true;
        }
        return false;
      });

      inputFile.files = dt.files;
      imagePreview.removeChild(previewContainer);
    });

    var previewContainer = document.createElement('div');
    previewContainer.classList.add('image-preview-container');
    previewContainer.appendChild(image);
    previewContainer.appendChild(deleteButton);

    // Add the image to the selectedImages array
    imagePreview.appendChild(previewContainer);
  };
}
