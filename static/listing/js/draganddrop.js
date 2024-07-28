// Add event listeners for drag and drop functionality
var dropzone = document.getElementById('dropzone');

// Get the file input element and the image preview container
var fileInput = document.getElementById('id_images');
var fileInput_pfp = document.getElementById('id_profile_image');
var imagePreview = document.getElementById('image-preview');
var selectedImages = [];

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

  if (fileInput) {
    // Get the selected files
    for (const file in e.dataTransfer.files) {
      if (Object.hasOwnProperty.call(e.dataTransfer.files, file)) {
        const element = e.dataTransfer.files[file];
        selectedImages.push(element);
      }
    }
    var dt = new DataTransfer();
    selectedImages.forEach(img => {
      dt.items.add(img);
    });
    var files = e.dataTransfer.files = fileInput.files = dt.files;
  }
  else if (fileInput_pfp) {
    // Handle the dropped files
    var files = e.dataTransfer.files;
    selectedImages.pop();
    selectedImages.push(files[0]);
  }
  // Clear the image preview container
  imagePreview.innerHTML = '';
  // Process the files as per your requirements, such as saving them to the database or storing them on the server
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    if (fileInput) {
      var inputFile = document.getElementById('id_images');
    }
    else if (fileInput_pfp) {
      var inputFile = document.getElementById('id_profile_image');
    }
      createImagePreview(file, inputFile);
  }
}

if (fileInput) {
  // Add an event listener to the file input element
  fileInput.addEventListener('change', function() {
    // Clear the image preview container
    imagePreview.innerHTML = '';
  
    // Get the selected files
    for (const file in fileInput.files) {
      if (Object.hasOwnProperty.call(fileInput.files, file)) {
        const element = fileInput.files[file];
        selectedImages.push(element);
      }
    }
    var dt = new DataTransfer();
    selectedImages.forEach(img => {
      dt.items.add(img);
    });
    var files = fileInput.files = dt.files;
  
    // Iterate over the selected files
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      var inputFile = document.getElementById('id_images');
      createImagePreview(file, inputFile);
    }
  });
}

if (fileInput_pfp) {
  // Add an event listener to the file input element
  fileInput_pfp.addEventListener('change', function() {
    // Clear the image preview container
    imagePreview.innerHTML = '';

    // Get the selected files
    var files = fileInput_pfp.files;

    // Iterate over the selected files
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      selectedImages.pop();
      selectedImages.push(file);
      var inputFile = document.getElementById('id_profile_image');
      createImagePreview(file, inputFile);
    }
  });
}

function createImagePreview(file, inputFile) {
  var reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function(e) {
    var image = document.createElement('img');
    image.classList.add('image-preview');
    image.src = e.target.result;
    image.alt = 'image' + e.target.result;

    var deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button', 'btn', 'btn-sm', 'mx-auto', 'mt-2');
    deleteButton.textContent = 'Remove';
    deleteButton.addEventListener('click', function () {
      var imageFile = inputFile.files[Array.from(imagePreview.children).indexOf(previewContainer)];
      var dt = new DataTransfer();
      selectedImages = selectedImages.filter(function (img) {
        if (img !== imageFile) {
          dt.items.add(img);
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

    imagePreview.appendChild(previewContainer);
  };
}
