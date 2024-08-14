// Add event listeners for drag and drop functionality
const dropzone = document.getElementById('dropzone');

// Get the file input element and the image preview container
const fileInput = document.getElementById('id_images');
const fileInput_pfp = document.getElementById('id_profile_image');
const imagePreview = document.getElementById('image-preview');
const selectedImages = [];

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
  let files;
  if (fileInput) {
    // Get the selected files
    for (const file in e.dataTransfer.files) {
      if (Object.hasOwnProperty.call(e.dataTransfer.files, file)) {
        const element = e.dataTransfer.files[file];
        selectedImages.push(element);
      }
    }
    const dt = new DataTransfer();
    selectedImages.forEach(img => {
      dt.items.add(img);
    });
    files = e.dataTransfer.files = fileInput.files = dt.files;
  }
  else if (fileInput_pfp) {
    // Handle the dropped files
    files = e.dataTransfer.files;
    selectedImages.pop();
    selectedImages.push(files[0]);
  }
  // Clear the image preview container
  imagePreview.innerHTML = '';
  // Process the files as per your requirements, such as saving them to the database or storing them on the server
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    let inputFile = null;
    if (fileInput) {
      inputFile = document.getElementById('id_images');
    }
    else if (fileInput_pfp) {
      inputFile = document.getElementById('id_profile_image');
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
    const dt = new DataTransfer();
    selectedImages.forEach(img => {
      dt.items.add(img);
    });
    const files = fileInput.files = dt.files;
  
    // Iterate over the selected files
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const inputFile = document.getElementById('id_images');
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
    const files = fileInput_pfp.files;

    // Iterate over the selected files
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      selectedImages.pop();
      selectedImages.push(file);
      const inputFile = document.getElementById('id_profile_image');
      $('#upload_input').attr('disabled', false);

      createImagePreview(file, inputFile);
    }

    if (imagePreview.innerHTML == '') {
      $('#upload_input').attr('disabled', true);
    }
  });
}

function createImagePreview(file, inputFile) {
  const reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function(e) {
    const image = document.createElement('img');
    image.classList.add('image-preview');
    image.src = e.target.result;
    image.alt = 'image' + e.target.result;

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button', 'btn', 'btn-sm', 'mx-auto', 'mt-2');
    deleteButton.textContent = 'Remove';
    deleteButton.addEventListener('click', function () {
      const imageFile = inputFile.files[Array.from(imagePreview.children).indexOf(previewContainer)];
      const dt = new DataTransfer();
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

    const previewContainer = document.createElement('div');
    previewContainer.classList.add('image-preview-container');
    previewContainer.appendChild(image);
    previewContainer.appendChild(deleteButton);

    imagePreview.appendChild(previewContainer);
  };
}
