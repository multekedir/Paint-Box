

function getData() {

}

function validateForm() {
  var x = document.forms["add_project"]["name"].value;
  if (x == "") {
    alert("Name must be filled out");
    return false;
  }
}

