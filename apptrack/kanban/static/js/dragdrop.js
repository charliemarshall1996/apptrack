const draggables = document.querySelectorAll(".task");
const droppables = document.querySelectorAll(".swim-lane");
const csrftoken = $('meta[name="csrf-token"]').attr('content');
var task_id= '0';
var emp_id = '0';


draggables.forEach((task) => {
  task.addEventListener("dragstart", () => {
    task.classList.add("is-dragging");
  });
  task.addEventListener("dragend", () => {
    task.classList.remove("is-dragging");
    
    get_assign(task_id, emp_id);

  });
});

droppables.forEach((zone) => {
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();

    const bottomTask = insertAboveTask(zone, e.clientY);
    const curTask = document.querySelector(".is-dragging");

    if (!bottomTask) {
      zone.appendChild(curTask);
    } else {
      zone.insertBefore(curTask, bottomTask);
    }
    task_id = curTask.id;
    emp_id = zone.id;
    });
});

const insertAboveTask = (zone, mouseY) => {
  const els = zone.querySelectorAll(".task:not(.is-dragging)");
  
  let closestTask = null;
  let closestOffset = Number.NEGATIVE_INFINITY;


  els.forEach((task) => {
    const { top } = task.getBoundingClientRect();

    const offset = mouseY - top;

    if (offset < 0 && offset > closestOffset) {
      closestOffset = offset;
      closestTask = task;
    }
  });

  return closestTask;
};

function get_assign(task_id, emp_id){
    get_request(emp_id, task_id)
    post_request(emp_id, task_id);
}

function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

function get_request(emp_id, task_id){
    $.ajax({
      type: 'GET',
      url: `/kanban/task-assign/${emp_id}/${task_id}/`,
      failure: function(data){
        console.log('failure');
        console.log(data);
      },
    });
  }

function post_request(emp_id, task_id){
    $.ajax({
      type: 'POST',
      url: `/kanban/task-assign/${emp_id}/${task_id}/`,
      failure: function(data){
        console.log('failure');
        console.log(data);
      },
    });
  }
//Inspired by https://github.com/TomIsLoading/drag-and-drop-kanban