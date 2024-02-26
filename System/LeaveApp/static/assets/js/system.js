function handleLeaveTypeChange() {
    var selectBox = document.getElementById("type_name");
    var otherLeaveInput = document.getElementById("other_leave_container"); // Changed the ID to match the container
    var otherLeaveTextbox = document.getElementById("other_leave");

    if (selectBox.value === "Other") {
        // If "Other" is selected, show the "Other leave" text box and enable it
        otherLeaveInput.style.display = "block"; // Show the container
        otherLeaveTextbox.disabled = false; // Enable the input
        otherLeaveTextbox.value = ""; // Clear the input value
    } else {
        // If any other option is selected, hide the "Other leave" text box and disable it
        otherLeaveInput.style.display = "none"; // Hide the container
        otherLeaveTextbox.disabled = true; // Disable the input
        otherLeaveTextbox.value = ""; // Clear the input value
    }
}




