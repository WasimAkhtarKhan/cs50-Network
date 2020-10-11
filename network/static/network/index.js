
    //document.addEventListener('DOMContentLoaded', function() {

        // Use buttons to toggle between views
    //    document.querySelector('#edit-btn').addEventListener('click', () => edit_post(id));
   
      
        //document.querySelector('#compose-form').onsubmit = send_email;   
    //  });
      
      
      
      function edit_post(id) {  
        document.querySelector(`#edit-form${id}`).style.display = 'block';
        document.querySelector(`#form-group${id}`).style.display = 'none';
      }
