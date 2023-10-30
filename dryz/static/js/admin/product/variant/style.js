
  document.addEventListener("DOMContentLoaded", function() {
     console.log("Button Clicked"); // Add this line
    const addVariantButton = document.getElementById("add_variant");
    const variantsContainer = document.getElementById("variants");

    addVariantButton.addEventListener("click", function() {
      const variantFields = document.createElement("div");
      variantFields.innerHTML = `
<div class="container my-4" style="background-color: rgb(176, 196, 222); padding: 20px; border-radius: 10px;">

    <!-- Weight -->
    <div class="form-group d-flex col-12 mx-1">
        <div class="col-6">
            <label for="variant_weight">Weight:</label>
                <input type="number" class="form-control" name="variant_weight[]" step="0.01" required>
            </div>
        <div class="col-6">
        <label for="variant_weight">Unit:</label>
        <select class="form-control" name="unit[]" required>
                             <option value="Kg">Kg</option>
                             <option value="Gm">Gm</option>
            </select>
        </div>
    </div>


    <div class="d-flex justify-content-between">

        <!-- Original Price -->
        <div class="form-group col-6">
            <label for="variant_original_price">Original price:</label>
            <input type="number" class="form-control" name="variant_original_price[]" step="0.01" required>
        </div>

        <!-- Selling Price -->
        <div class="form-group col-6">
            <label for="variant_selling_price">Selling Price:</label>
            <input type="number" class="form-control" name="variant_selling_price[]" step="0.01" required>
        </div>
    </div>

    <!-- Stock -->
    <div class="form-group">
        <label for="variant_stock">Stock:</label>
        <input type="number" class="form-control" name="variant_stock[]" step="0.01" required>
    </div>
</div>
      `;
      variantsContainer.appendChild(variantFields);

    });
  });