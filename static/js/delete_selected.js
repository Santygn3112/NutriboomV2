document.getElementById('deleteSelectedBtn').addEventListener('click', function() {
   var form = document.getElementById('deleteSelectedForm');

       document.getElementById('confirmDeleteBtn').onclick = function() {
           form.submit();
       };
   
});
