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
      // Create a URL for the blob object
      const imageUrl = URL.createObjectURL(blob);

      // Display the image
      document.getElementById("resultImage").src = imageUrl;
    })
    .catch((error) => console.error("Error fetching data:", error));
});
