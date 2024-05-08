document.getElementById("uploadForm").addEventListener("submit", function (event) {
  event.preventDefault();

  // Create a FormData object, passing the form as a parameter
  const formData = new FormData(event.target);

  // Append 'h' if it's not set (or you could handle this in the backend)
  if (!formData.has("h") || formData.get("h").trim() === "") {
    formData.set("h", "0.03");
  }

  // Perform the Fetch request
  fetch("http://localhost:8000/process_image", {
    method: "POST",
    body: formData, // FormData object
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.blob(); // Assuming server returns a file
    })
    .then((blob) => {
      // Create a Blob URL from the returned blob
      const url = URL.createObjectURL(blob);

      // Optionally download the image or display it
      const downloadLink = document.createElement("a");
      downloadLink.href = url;
      downloadLink.download = "processed_image.png";
      downloadLink.click();

      // Revoke the Blob URL to free up resources
      URL.revokeObjectURL(url);
    })
    .catch((error) => console.error("Error fetching data:", error));
});
