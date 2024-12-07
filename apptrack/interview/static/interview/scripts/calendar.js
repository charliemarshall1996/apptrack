document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var interviews = document.getElementById("interviews_json").value;
  console.log(interviews);
  var events = JSON.parse(String(interviews));
  function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  };
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: events,
    selectable: true,
    eventClick: function(info) {
        var event = info.event;
        var eventId = event.id;
    	console.log("Event ID:", eventId);

        // Make an AJAX request to fetch interview details
        fetch(`/interview/event-detail/${eventId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {alert('Error: ' + data.error);} 
				else {
					// Populate the modal with interview data
					document.getElementById('viewInterviewLabel').textContent = `Interview Details for ${data.title}`;
					var modalBodyContent = document.querySelector('#viewInterview .modal-body-content');
					var taskList = document.querySelector('#viewInterview .list-group');

					
					// Clear previous content (if any)
					modalBodyContent.innerHTML = '';

					// Fill modal with interview data
					modalBodyContent.innerHTML += `<div class="row"><div class="col"><p><strong>Job Title:</strong> ${data.title}</p></div><div class="col"><p><strong>Company:</strong> ${data.company}</p></div></div>`;
					modalBodyContent.innerHTML += `<div class="row"><div class="col"><p><strong>Date:</strong> ${data.date}</p></div></div>`;
					modalBodyContent.innerHTML += `<div class="row"><div class="col"><p><strong>Start Time:</strong> ${data.start_time}</p></div><div class="col"><p><strong>End Time:</strong> ${data.end_time}</p></div></div>`;
					modalBodyContent.innerHTML += `<div class="row"><div class="col"><p><strong>Notes:</strong> ${data.notes}</p></div></div>`;
					
					// Show the modal
					
					taskList.innerHTML = '';
					// Fetch tasks and populate the task list
					data.tasks.forEach(task => {

						const taskItem = document.createElement('li');
						taskItem.classList.add('list-group-item');

						const taskForm = document.createElement('form');
						taskForm.method = 'POST';
						taskForm.action = '';
						taskForm.form

						const formType = document.createElement('input');
						formType.type = 'hidden';
						formType.name = 'form_type';
						formType.value = 'update_task';

						const checkBox = document.createElement('input')
						checkBox.type = 'checkbox';
						checkBox.checked = task.completed;

						const row = document.createElement('div');
						row.classList.add('row');

						const col1 = document.createElement('div');
						const col2 = document.createElement('div');

						const name = document.createElement('span');
						name.textContent = task.name;
						col1.classList.add('col');
						col2.classList.add('col');
						col1.appendChild(name);
						col2.appendChild(checkBox);
						row.appendChild(col1);
						row.appendChild(col2);
						taskItem.appendChild(row);
						taskList.appendChild(taskItem);

						checkBox.addEventListener('change', function() {
							const isCompleted = this.checked;
							const taskId = task.id;

							fetch(`/interview/calendar/`, {
								method: 'POST',
								headers: {
									'Content-Type': 'application/json',
									'X-CSRFToken': getCSRFToken(),
								},
								body: JSON.stringify({
									form_type: 'update_task',
									task_id: taskId,
									completed: isCompleted
								})
                                                            
                              
                            }); 
                        });
                	});

						const taskItem = document.createElement('a');
						const row = document.createElement('div');
						const col = document.createElement('div');
						const txt = document.createElement('span');
						
						row.classList.add('row');
						row.classList.add('text-center');
						col.classList.add('col');
						txt.innerHTML = `<p class="display-5"><strong>+</strong></p>`;
						
						taskItem.classList.add('list-group-item');
						taskItem.classList.add('list-group-item-action');
						taskItem.href = `#`;
						col.appendChild(txt);
						row.appendChild(col);
						taskItem.appendChild(row);
						taskList.appendChild(taskItem);

						var viewInterviewModal = new bootstrap.Modal(document.getElementById('viewInterview'));
						viewInterviewModal.show();
                      	}
                  	})
					.catch(error => {
						console.error('Error fetching interview details:', error);
						alert('An error occurred while fetching the interview details.');
                  	});
          	}
  	});
  
  calendar.render();
});