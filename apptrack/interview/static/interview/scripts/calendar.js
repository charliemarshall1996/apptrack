document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var data = duc
    var interviews = JSON.parse(document.getElementById('interview-data'));
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: interviews
    });
    calendar.render();
  });