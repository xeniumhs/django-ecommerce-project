document.addEventListener("DOMContentLoaded", function () {
  const zoomImages = document.querySelectorAll(".zoom-img"); // Get all images with class zoom-img

  zoomImages.forEach((zoomImage) => {
    const imageContainer = zoomImage.closest(".image-container"); // Find the parent container of each image
    const zoomLens = document.createElement("div");
    zoomLens.classList.add("zoom-lens");
    imageContainer.appendChild(zoomLens);

    // Set a fixed size for the zoom lens for consistency
    zoomLens.style.width = "100px"; // Adjust as needed
    zoomLens.style.height = "100px"; // Adjust as needed

    zoomImage.addEventListener("mousemove", function (e) {
      const containerRect = imageContainer.getBoundingClientRect();

      // Mouse position relative to the container
      const offsetX = e.clientX - containerRect.left;
      const offsetY = e.clientY - containerRect.top;

      // Position the zoom lens over the mouse position
      zoomLens.style.left = `${Math.min(
        Math.max(offsetX - zoomLens.offsetWidth / 2, 0),
        imageContainer.offsetWidth - zoomLens.offsetWidth
      )}px`;
      zoomLens.style.top = `${Math.min(
        Math.max(offsetY - zoomLens.offsetHeight / 2, 0),
        imageContainer.offsetHeight - zoomLens.offsetHeight
      )}px`;

      // Show the zoom lens when hovering
      zoomLens.style.display = "block";

      // Calculate the zoom position based on where the lens is
      const lensWidth = zoomLens.offsetWidth;
      const lensHeight = zoomLens.offsetHeight;

      // Set the background position and zoom effect for each image
      const backgroundPosX = (offsetX / imageContainer.offsetWidth) * 100;
      const backgroundPosY = (offsetY / imageContainer.offsetHeight) * 100;

      // Apply zoom effect and adjust the origin to the lens' position
      zoomImage.style.transform = `scale(2)`; // Increase scale for zoom
      zoomImage.style.transformOrigin = `${backgroundPosX}% ${backgroundPosY}%`;
    });

    imageContainer.addEventListener("mouseleave", function () {
      // Hide the lens when mouse leaves the image
      zoomLens.style.display = "none";
      zoomImage.style.transform = "scale(1)"; // Reset zoom
    });
  });
});
