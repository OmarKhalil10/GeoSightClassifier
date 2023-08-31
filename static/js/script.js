document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form"); // Get the form by its id
    const classifyButton = document.getElementById("classify-button");
    const uploadedImage = document.getElementById("uploaded-image");
    const predictionsSection = document.querySelector(".predictions-section");
    const imageSection = document.querySelector(".image-section");

    classifyButton.addEventListener("click", function () {
        const formData = new FormData(form); // Create FormData from the form

        fetch("/predict", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                // Update the UI with the response data
                if (data.image_path) {
                    // Update the image src only if a new image is provided
                    uploadedImage.src = data.image_path;
                }

                // Clear previous predictions
                const predictionsTable = document.getElementById("predictions-table");
                predictionsTable.innerHTML = "";

                // Add new predictions to the table
                data.classes.forEach((className, index) => {
                    const row = predictionsTable.insertRow(index);
                    const classCell = row.insertCell(0);
                    const probCell = row.insertCell(1);

                    classCell.textContent = className;
                    probCell.textContent = `${(data.probs[index] * 100).toFixed(2)}%`;
                });

                // Show the image and predictions section
                imageSection.style.display = "block";
                predictionsSection.style.display = "block";
            })
            .catch((error) => {
                // Handle any errors here
                console.error("Error:", error);
            });
    });
});
