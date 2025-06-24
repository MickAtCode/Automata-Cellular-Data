document.addEventListener("DOMContentLoaded", function () {
  const inpFile = document.getElementById("input-file");
  const fview = document.getElementById("file-view");
  const fileList = document.getElementById("file-list");

  // Trigger file input click when file-view is clicked
  fview.addEventListener("click", function () {
    inpFile.click();
  });

  inpFile.addEventListener("change", function (event) {
    // Clear the file list before adding new files
    fileList.innerHTML = "";

    // Get the selected files
    const files = event.target.files;

    // Display the selected files
    if (files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        const listItem = document.createElement("li");
        listItem.textContent = files[i].name; // Display the name of the file
        fileList.appendChild(listItem);
      }
    } else {
      const listItem = document.createElement("li");
      listItem.textContent = "No files chosen"; // Message if no files are chosen
      fileList.appendChild(listItem);
    }

    fview.style.display = "block"; // Ensure the file view is displayed
  });
});
