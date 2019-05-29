function get_projects(handleData) {
    $.ajax({
        type: "GET",
        url: "/get_projects",
        cache: false,
        data: $('form#addProjectForm').serialize(),
        success: function (response) {
            var data = JSON.parse(response);
            handleData(data); 
            // console.log(data);
            //
            // for (i = 0; i <data.length; i++) {
            //      console.log(data[i].name);
            // }
        },
        error: function (response) {
            console.log('ERROR');
            console.log(response);
        }

    });
}
function toggleSidebar(){
    // open or close navbar
        $('#sidebar,    #content').toggleClass('active');
        // close dropdowns
        $('.collapse.in').toggleClass('in');
        // and also adjust aria-expanded attributes we use for the open/closed arrows
        // in our CSS
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
}


function modal_message(headerText,alertText, buttonText) {
    let header = document.getElementById("message-header");
    header.innerText = headerText;
    let message = document.getElementById("alert-message");
    message.innerText = alertText;
    let button = document.getElementById('submit');

    if (buttonText == "save"){
        button.classList.add("btn-success");
        button.innerText = "Save"
    }else {
        button.classList.add("btn-danger");
        button.innerText = "Delete"
    }
    $('#message').modal('show');

}

function modal_button(action) {
      $('#submit').on('click',function () {
          action();
        $('#message').modal('hide');

    });

    $('#dismiss').on('click',function () {
        $('#message').modal('hide');
        location.reload();
    });

}


function divClicked() {
    let divHtml = $('#editDescription').html();
    let editableText = $("<textarea />");
    editableText.val(divHtml);
   $('#editDescription').replaceWith(editableText);
    editableText.focus();
    $('#editDescription').addClass('md-textarea form-control')
    // setup the blur event for this new textarea
    editableText.blur(write_description);
}

function write_description() {
    let html = $(this).val().replace(/\n/g, "");
    let viewableText = $("<p>");
    let pro = document.getElementById('submit').getAttribute('project_id')
    viewableText.html(html);
    $(this).replaceWith(viewableText);
    $(this).replaceWith(viewableText);
    modal_message("Save Description","Do you want to save?","save");
    viewableText.click(divClicked);
    modal_button(function (){
        $.ajax({
            type: "POST",
            url: "save_description/" + pro,
            cache: false,
            data: {'desc':html},
        success: function (response) {
            window.location.href = response['redirect'];
        },
        error: function (response) {
            console.log(response);
        }

    });
    });

}



$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        if ( window.innerWidth < 769){
            toggleSidebar();
        }

    });

    $('#editDescription').on('click',divClicked);

    // get_projects();
    // for (i = 0; i <bob.length; i++) {
    //              console.log(bob[i].name);
    //         }

    // $("#addProjectForm").submit(function(event){
    // 	return test();
    // });

});





function delete_project() {
    modal_message('Deleting Project','Are sure you want to delete the project?','delete');
    let pro = document.getElementById('submit').getAttribute('project_id')
    modal_button(function (){
        $.ajax({
        type: "POST",
        url: "delete/" + pro,
        cache: false,
        data: {'id':pro},
        success: function (response) {
              window.location.href = response['redirect'];
        },
        error: function (response) {
            console.log(response);
        }

    });
    });
}

function upload_file() {
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: $('form#uploadFileForm').serialize(),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
            },
        });
}

function addProject() {

    out = false;
    $.ajax({
        async:false,
        type: "POST",
        url: "/add_project",
        cache: false,
        data: $('form#addProjectForm').serialize(),
        success: function (response) {
            console.log("success");
            console.log(response['added']);
            if (response['added'] != false) {
                console.log(response['messages'])
                out = true;

            }else {
                document.getElementById('errors').innerHTML = response['messages']
                 document.getElementById('errors').classList.add('visible')
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
            out = false;
        }

    });

    return out;
}

function addStage(id) {
    let out = false;
    $.ajax({
        async:false,
        type: "POST",
        url: "/add_stage/"+id,
        cache: false,
        data: $('form#addStageForm').serialize(),
        success: function (response) {
            console.log("success"+response['added']);
            if (response['added'] != false) {
                console.log(response['messages'])
                out = true;

            }else {
                document.getElementById('errors').innerHTML = response['messages'];
                 document.getElementById('errors').classList.add('visible');
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
            out = false;
        }

    });

    return out;
}