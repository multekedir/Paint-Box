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

$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        // open or close navbar
        $('#sidebar,    #content').toggleClass('active');
        // close dropdowns
        $('.collapse.in').toggleClass('in');
        // and also adjust aria-expanded attributes we use for the open/closed arrows
        // in our CSS
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    // get_projects();
    // for (i = 0; i <bob.length; i++) {
    //              console.log(bob[i].name);
    //         }

    // $("#addProjectForm").submit(function(event){
    // 	return test();
    // });

});

//
// function test() {
//     alert('do');
//     return true;
// }



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