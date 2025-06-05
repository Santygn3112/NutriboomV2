

function checkAll(selectAllCheckbox) {
    // Selecciona únicamente los checkboxes de la tabla (los de los platos)
    const checkboxes = document.querySelectorAll(
      'table tbody input[type="checkbox"][name="ids"]'
    );
   
   
    checkboxes.forEach(function (checkbox) {
      checkbox.checked = selectAllCheckbox.checked;
    });
   }
   