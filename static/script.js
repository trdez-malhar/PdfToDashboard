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

        $("#status").text(""); 
        $("#loading").show();  
        $("button").prop("disabled", true); 

        let startTime = new Date().getTime(); // Start time

        let timer = setInterval(() => {
            let elapsedTime = ((new Date().getTime() - startTime) / 1000).toFixed(1);
            $("#loading").text(`Uploading... Please wait. Time elapsed: ${elapsedTime} sec`);
        }, 100); // Update every 100ms

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                clearInterval(timer); // Stop the timer
                $("#loading").text("Upload complete! Redirecting...");
                setTimeout(() => {
                    window.location.href = "/dashboard";
                }, 1000);
            },
            error: function() {
                clearInterval(timer); 
                $("#status").text("An error occurred.");
                $("#loading").hide();
                $("button").prop("disabled", false);
            }
        });
    });
});
