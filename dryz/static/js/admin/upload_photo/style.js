<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        $("#img").attr("src", e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
    }
  }