// Get CSRF token from the meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Select draggable jobs and columns
const draggables = document.querySelectorAll(".job");
const droppables = document.querySelectorAll(".card-body"); // Change to card-body where jobs are located
let job_id = null;

// Add event listeners for dragstart and dragend
draggables.forEach((job) => {
  job.addEventListener("dragstart", () => {
    job.classList.add("is-dragging");
    job_id = job.id;  // Store the job ID when dragging starts
  });

  job.addEventListener("dragend", () => {
    job.classList.remove("is-dragging");
    get_assign(job_id);  // Send job ID to backend after drop
  });
});

// Add event listeners for dragover and drop on each column
droppables.forEach((column) => {
  column.addEventListener("dragover", (e) => {
    e.preventDefault();  // Allow dropping
    const bottomJob = insertAboveJob(column, e.clientY);  // Get the position of the job
    const curJob = document.querySelector(".is-dragging");

    // Append or insert dragged job at the correct location
    if (!bottomJob) {
      column.appendChild(curJob);
    } else {
      column.insertBefore(curJob, bottomJob);
    }
  });
});

// Function to find the position to insert the dragged job
const insertAboveJob = (column, mouseY) => {
  const jobs = column.querySelectorAll(".job:not(.is-dragging)");

  let closestJob = null;
  let closestOffset = Number.NEGATIVE_INFINITY;

  jobs.forEach((job) => {
    const { top } = job.getBoundingClientRect();
    const offset = mouseY - top;

    if (offset < 0 && offset > closestOffset) {
      closestOffset = offset;
      closestJob = job;
    }
  });

  return closestJob;
};

// Function to send the updated job position to the server
function get_assign(job_id) {
  send_request(job_id);
}

// Setup AJAX to include CSRF token
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);  // Use correct CSRF token
    }
  }
});

// Function to send the AJAX request to update the job position
function send_request(job_id) {
  $.ajax({
    type: 'POST',  // Use POST to update data
    url: moveJobUrl,  // Defined in the template
    data: {
      'job_id': job_id,  // Send job ID to the server
      'column_id': document.querySelector(".is-dragging").closest(".card-body").getAttribute('data-column-id') // Send new column ID
    },
    success: function (data) {
      console.log('Job moved successfully');
      console.log(data);
    },
    error: function (data) {
      console.error('Error moving job');
      console.error(data);
    }
  });
}
