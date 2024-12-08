document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var interviews = document.getElementById("interviews_json").value;
  var events = JSON.parse(String(interviews));
  function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  };
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: events,
    selectable: true,
    eventClick: function(info) {
		// Construct the modal ID from the event ID
		var modalId = '#viewInterviewModal' + info.event.id;
	
		// Show the modal corresponding to the clicked event
		var modal = new bootstrap.Modal(document.querySelector(modalId));
		modal.show();
		var tasks = document.querySelectorAll(`${modalId} #taskList .list-group-item .checkbox input`);
		console.log("tasks", tasks);
		tasks.forEach(task => {
			const taskId = task.id.replace('taskCheckbox', '');
			task.addEventListener("change", function() {
				if (this.checked) {
					fetch(`/interview/update-task/${taskId}/`, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': getCSRFToken()
						},
						body: JSON.stringify({'completed': true})
					}).then(response => {
						if (response.ok) {
							console.log('Task updated successfully');
						} else {
							console.error('Failed to update task');
						}
					})
				} else {
					fetch(`/interview/update-task/${taskId}/`, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': getCSRFToken()
						},
						body: JSON.stringify({'completed': false})
					}).then(response => {
						if (response.ok) {
							console.log('Task updated successfully');
						} else {
							console.error('Failed to update task');
						}
					})
				}
			});
			
		});
		
	  }
	});

	
  
  calendar.render();
});