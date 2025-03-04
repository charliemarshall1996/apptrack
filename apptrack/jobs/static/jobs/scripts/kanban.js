const draggables = document.querySelectorAll(".task");
const droppables = document.querySelectorAll(".swim-lane");
const csrftoken = $('meta[name="csrf-token"]').attr('content');
var job_id= '0';
var emp_id = '0';

// Allow the column to accept a drop
function allowDrop(ev) {
  ev.preventDefault(); // Prevent the default behavior
}

// Start dragging the job card
function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id); // Store the dragged element's ID
}

draggables.forEach((task) => {
  task.addEventListener("dragstart", () => {
    task.classList.add("is-dragging");
  });
  task.addEventListener("dragend", () => {
    task.classList.remove("is-dragging");
    
    get_assign(job_id, emp_id);

  });
});

droppables.forEach((zone) => {
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();

    const bottomTask = insertAboveTask(zone, e.clientY);
    const curTask = document.querySelector(".is-dragging");

    if (bottomTask) {
      zone.appendChild(curTask);
    } else {
      zone.insertBefore(curTask, bottomTask);
    }
    job_id = curTask.id;
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

function get_assign(job_id, emp_id){
    post_request(emp_id, job_id);
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


function post_request(col_id, job_id){
  $.ajax({
    type: 'POST',
    url: `/jobs/assign/${col_id}/${job_id}/`,
    success: function(data) {
      console.log('Post successful', data);
      if (data.job_status == 'RE') {
        showArchiveModal(data.job_id);
      } else if (data.job_status == 'CL') {
        showArchiveModal(data.job_id);
      };
      window.location.reload();
      
      
    },
    error: function(xhr, status, error) {
      console.log('Error:', error);
      console.log('XHR:', xhr);
      console.log('Status:', status);
    }
  });
}

function showArchiveModal(jobID){
  const modalElement = document.getElementById('archiveJobModal');
  const modal = new bootstrap.Modal(modalElement);
  
  modal.show();
  document.getElementById('jobIdToArchive').value = jobID;
}

function showFeedbackModal(jobID){
  const modalElement = document.getElementById('feedbackModal');
  const modal = new bootstrap.Modal(modalElement);
  document.getElementById('jobIdToFeedback').value = jobID;
  modal.show();
}