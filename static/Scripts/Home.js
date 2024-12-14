document.getElementById("freelancer").addEventListener("click", function () {
    window.location.href = "/freelancer"; // Flask route for the freelancer form
});

document.getElementById("companies").addEventListener("click", function () {
    window.location.href = "/jobs"; // Flask route for the jobs form
});

document.getElementById("rate").addEventListener("input", function (e) {
    const value = parseFloat(e.target.value);
    if (value < 0 || value > 5) {
        alert("Rating must be between 0 and 5.");
    }
});