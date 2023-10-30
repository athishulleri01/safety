<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

$(document).ready(function () {
    // Select all OTP input fields
    const otpInputs = $(".otp-input");

    // Add input event listener for OTP inputs
    otpInputs.on("input", function () {
        const input = $(this);
        const value = input.val();

        // Validate input: Allow only numeric characters
        const isValid = /^\d*$/.test(value);

        if (!isValid) {
            // Clear input if it's not a valid numeric character
            input.val("");
        } else {
            // Move focus to the next input field if this one has a valid character
            const index = otpInputs.index(input);
            if (index < otpInputs.length - 1 && value !== "") {
                otpInputs.eq(index + 1).focus();
            }

            // Check if the input has a value and add the "has-value" class for green border
            if (value !== "") {
                input.addClass("has-value");
            } else {
                input.removeClass("has-value");
            }
        }
    });

    // Add focus event listener to apply green border when clicked
    otpInputs.on("focus", function () {
        $(this).addClass("border border-success"); // Add green border
    });

    // Add blur event listener to remove green border when focus is lost
    otpInputs.on("blur", function () {
        $(this).removeClass("border border-success"); // Remove green border
    });

    // Add paste event listener to automatically fill OTP fields
    otpInputs.on("paste", function (e) {
        const pastedText = e.originalEvent.clipboardData.getData("text");
        if (/^\d{6}$/.test(pastedText)) {
            const digits = pastedText.split("");
            otpInputs.each(function (index) {
                $(this).val(digits[index]);
                $(this).addClass("has-value");
            });
        }
        e.preventDefault();
    });

    // Clear button click event
    $("#clearButton").on("click", function () {
        otpInputs.val("").removeClass("has-value");
        otpInputs.eq(0).focus(); // Set focus back to the first OTP input field
    });
});
