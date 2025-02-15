$(document).ready(function() {
    $("#uploadForm").submit(function(event) {
        event.preventDefault();

        let fileInput = $("#fileInput")[0].files[0];
        if (!fileInput) {
            $("#status").text("Please select a file.");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput);

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $("#status").text(response.message);
                
                window.location.href = "http://127.0.0.1:5000/dashboard";
            },
            error: function() {
                $("#status").text("An error occurred.");
            }
        });
    });
});
