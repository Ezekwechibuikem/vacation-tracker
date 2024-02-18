document.addEventListener("DOMContentLoaded", function() {
    var startDateInput = document.getElementById("start-date");
    var endDateInput = document.getElementById("end-date");
    var totalDaysInput = document.getElementById("total-days");
    var resumptionDateInput = document.getElementById("resumption-date");

    // Function to calculate number of days between two dates
    function calculateNumberOfDays() {
        var startDate = new Date(startDateInput.value);
        var endDate = new Date(endDateInput.value);
        var differenceInTime = endDate.getTime() - startDate.getTime();
        var differenceInDays = differenceInTime / (1000 * 3600 * 24);
        totalDaysInput.value = differenceInDays;

        // Calculate resumption date
        var resumptionDate = new Date(endDate);
        resumptionDate.setDate(resumptionDate.getDate() + 1); // Add one day
        if (resumptionDate.getDay() === 0 || resumptionDate.getDay() === 6) {
            // If the next day is a weekend, move to the next working day
            resumptionDate.setDate(resumptionDate.getDate() + (8 - resumptionDate.getDay()));
        }
        resumptionDateInput.value = resumptionDate.toDateString();
    }

    // Event listeners for date inputs
    startDateInput.addEventListener("change", calculateNumberOfDays);
    endDateInput.addEventListener("change", calculateNumberOfDays);
});


