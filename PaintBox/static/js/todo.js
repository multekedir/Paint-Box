function showTodo(id) {
	$('#todo_modal').modal('show');
	$('#add_button').attr('stage_id', id);
	get_started();
	get_completed();
}

var taskInput=document.getElementById("new-task");//Add a new task.
var addButton=document.getElementById("add_button");//first button
var incompleteTaskHolder=document.getElementById("incomplete-tasks");//ul of #incomplete-tasks
var completedTasksHolder=document.getElementById("completed-tasks");//completed-tasks


//New task list item
var createNewTaskElement=function(taskString, taskID){

	let listItem=document.createElement("li");
	listItem.setAttribute("task_id",taskID);

	//input (checkbox)
	let checkBox=document.createElement("input");//checkbx
	checkBox.setAttribute("task_id",taskID);
	//label
	let label=document.createElement("label");//label
	label.setAttribute("task_id",taskID);
	//input (text)
	let editInput=document.createElement("input");//text
	editInput.setAttribute("task_id",taskID);
	//button.edit
	let editButton=document.createElement("button");//edit button
	editButton.setAttribute("task_id",taskID);

	//button.delete
	let deleteButton=document.createElement("button");//delete button
	deleteButton.setAttribute("task_id",taskID);

	label.innerText=taskString;

	//Each elements, needs appending
	checkBox.type="checkbox";
	editInput.type="text";

	editButton.innerText="Edit";//innerText encodes special characters, HTML does not.
	editButton.className="edit";
	deleteButton.innerText="Delete";
	deleteButton.className="delete";



	//and appending.
	listItem.appendChild(checkBox);
	listItem.appendChild(label);
	listItem.appendChild(editInput);
	listItem.appendChild(editButton);
	listItem.appendChild(deleteButton);
	return listItem;
}


var addTask=function(){
	console.log("Add Task...");

	  let out = false;
    $.ajax({
        async:false,
        type: "POST",
        url: "/add_task/"+$('#add_button').attr('stage_id'),
        cache: false,
        data: {'name':taskInput.value},
        success: function (response) {
            console.log("success"+response['added']);
            if (response['added'] != false) {
                console.log(response['messages'])
				//Create a new list item with the text from the #new-task:
				let listItem=createNewTaskElement(taskInput.value, response['taskid']);

				//Append listItem to incompleteTaskHolder
				incompleteTaskHolder.appendChild(listItem);
				bindTaskEvents(listItem, taskCompleted);
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
	taskInput.value="";
    return out;


}

//Edit an existing task.

var editTask=function(){
	console.log("Edit Task...");
	console.log("Change 'edit' to 'save'");
	this.innerText = "Save"
	let listItem=this.parentNode;

	let editInput=listItem.querySelector('input[type=text]');
	let label=listItem.querySelector("label");
	let containsClass=listItem.classList.contains("editMode");
	//If class of the parent is .editmode
	if(containsClass){

	//switch to .editmode
	//label becomes the inputs value.
		label.innerText=editInput.value;
		this.innerText = "Edit"
	}else{
		editInput.value=label.innerText;
	}

	//toggle .editmode on the parent.
	listItem.classList.toggle("editMode");
}


//Delete task.
var deleteTask=function(){
		console.log("Delete Task...");

		var listItem=this.parentNode;
		var ul=listItem.parentNode;
		//Remove the parent list item from the ul.
		ul.removeChild(listItem);

}


//Mark task completed
var taskCompleted=function(){
	console.log("Complete Task...");

	//Append the task list item to the #completed-tasks
	var listItem=this.parentNode;
	completedTasksHolder.appendChild(listItem);
	bindTaskEvents(listItem, taskIncomplete);
	$.ajax({
        type: "POST",
        url: "/complete_task/"+$('#add_button').attr('stage_id')+"/"+$(this).attr('task_id'),
        cache: false,
        data: {},
        success: function (response) {
            console.log("success "+response['added']);
            if (response['completed'] != false) {
            	console.log("Done")

            }else {
                document.getElementById('errors').innerHTML = response['messages'];
                 document.getElementById('errors').classList.add('visible');
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
        }

    });
}


var taskIncomplete=function(){
	console.log("Incomplete Task...");
	//Mark task as incomplete.
	//When the checkbox is unchecked
	//Append the task list item to the #incomplete-tasks.
	var listItem=this.parentNode;
	incompleteTaskHolder.appendChild(listItem);
	bindTaskEvents(listItem,taskCompleted);
	$.ajax({
        type: "POST",
        url: "/incomplete_task/"+$('#add_button').attr('stage_id')+"/"+$(this).attr('task_id'),
        cache: false,
        data: {},
        success: function (response) {
            console.log("success "+response['added']);
            if (response['completed'] != false) {
            	console.log("Done")

            }else {
                document.getElementById('errors').innerHTML = response['messages'];
                document.getElementById('errors').classList.add('visible');
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
        }

    });
}


function get_completed() {
	console.log("Getting completed Tasks...");
	// clear all tasks
	$("#completed-tasks").empty();

    $.ajax({
        type: "POST",
        url: "/get_completed/"+$('#add_button').attr('stage_id'),
        cache: false,
        data: {},
        success: function (response) {
            console.log("success "+response['added']);
            if (response['added'] != false) {
            	let names = response['payload_name']
				let ids = response['payload_id']
                for (i = 0; i < response['payload_name'].length; i++) {
  					let listItem=createNewTaskElement(names[i],ids[i]);
					completedTasksHolder.appendChild(listItem);
					bindTaskEvents(listItem, taskIncomplete);
				}

            }else {
                document.getElementById('errors').innerHTML = response['messages'];
                 document.getElementById('errors').classList.add('visible');
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
        }

    });
}


function get_started() {
	console.log("Getting incomplete Tasks...");
	// clear all tasks
	$("#incomplete-tasks").empty();

    $.ajax({
        type: "POST",
        url: "/get_started/"+$('#add_button').attr('stage_id'),
        cache: false,
        data: {},
        success: function (response) {
            console.log("success "+response['added']);
            if (response['added'] != false) {
            	let names = response['payload_name']
				let ids = response['payload_id']
                for (i = 0; i < response['payload_name'].length; i++) {
  					let listItem=createNewTaskElement(names[i],ids[i]);
					incompleteTaskHolder.appendChild(listItem);
					bindTaskEvents(listItem, taskCompleted);
				}

            }else {
                document.getElementById('errors').innerHTML = response['messages'];
                 document.getElementById('errors').classList.add('visible');
                document.getElementById('errors').classList.remove('invisible')
                console.log(response['messages'])
            }

        },
        error: function (response) {
            console.log(response);
        }

    });
	taskInput.value="";
}

var bindTaskEvents=function(taskListItem,checkBoxEventHandler){
	console.log("bind list item events");
//select ListItems children
	var checkBox=taskListItem.querySelector("input[type=checkbox]");
	var editButton=taskListItem.querySelector("button.edit");
	var deleteButton=taskListItem.querySelector("button.delete");


			//Bind editTask to edit button.
			editButton.onclick=editTask;
			//Bind deleteTask to delete button.
			deleteButton.onclick=deleteTask;
			//Bind taskCompleted to checkBoxEventHandler.
			checkBox.onchange=checkBoxEventHandler;
}

//cycle over incompleteTaskHolder ul list items
	//for each list item
	for (var i=0; i<incompleteTaskHolder.children.length;i++){

		//bind events to list items chldren(tasksCompleted)
		bindTaskEvents(incompleteTaskHolder.children[i],taskCompleted);
	}




//cycle over completedTasksHolder ul list items
	for (var i=0; i<completedTasksHolder.children.length;i++){
	//bind events to list items chldren(tasksIncompleted)
		bindTaskEvents(completedTasksHolder.children[i],taskIncomplete);
	}




// Issues with usabiliy don't get seen until they are in front of a human tester.

//prevent creation of empty tasks.

//Shange edit to save when you are in edit mode.