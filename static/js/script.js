document.getElementById('downloadImageBtn').addEventListener('click', function () {
  const designImage = document.getElementById('designImage');
  if (designImage.src) {
    const a = document.createElement('a');
    a.href = designImage.src;
    a.download = 'small_box_image.png'; // Specify the file name
    a.click();
  } else {
    alert('No image to download!');
  }
});

// Function to get the query parameter value
function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

// Get the download URL (image URL) from the query parameter
const downloadURL = getQueryParam('downloadURL');

// If a downloadURL is passed, set it as the source for the image
if (downloadURL) {
  const imgElement = document.getElementById('designImage');
  imgElement.src = decodeURIComponent(downloadURL); // Set the src to the image URL
}

// Get elements from the DOM
const color = document.querySelector(".color");
const colorSelect = document.querySelector(".color-select"); // Change to select element
const colorBox = document.querySelector(".color-box"); // Select the new color box

// Add change event listener for the dropdown
colorSelect.addEventListener("change", () => {
  // Get the selected color value from the dropdown
  const selectedColor = colorSelect.value;

  // Update the shirt overlay and the color box with the selected color
  color.style.backgroundColor = selectedColor;
  colorBox.style.backgroundColor = selectedColor;
});
