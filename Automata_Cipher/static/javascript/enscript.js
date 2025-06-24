const inpFile = document.getElementById("input-file");
const fview = document.getElementById("file-view");

// Combined event listener to display file name and handle file upload
inpFile.addEventListener("change", function (event) {
  // Display the selected file name
  const fileName = event.target.files[0]?.name || "No file chosen";
  fview.querySelector("span").textContent = fileName;

  // Optional: Upload file logic
  uploadFile(event.target.files[0]); // Pass the file to uploadFile function
});

function uploadFile(file) {
  if (file) {
    console.log("File selected:", file.name);
    fview.style.display = "block";
  }
}
