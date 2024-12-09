

$.ajax({ 
    method: "GET", 
    url: userStreakEndpoint,
    success: function(data) {
        console.log("data ", data);
        if (data.target > 0) {
            console.log("target " + data.target);
            displayStreakData(data, 'currentUnit');
            displayStreakData(data, 'currentApplications');
            displayStreakData(data, 'targetAmount');
            displayStreakData(data, 'currentStreak');
            displayStreakData(data, 'streakUnit');

        }
      
    }, 
    error: function(error_data) { 
      console.log(error_data); 
    } 
  });
  function displayStreakData(data, id) {
    var statData = "";
    var statElement = document.getElementById(id);
    if (id == "currentUnit") {
        statData = data.unit;
    } else if (id == "currentApplications") {
        statData = data.current_applications;
    } else if (id == "targetAmount") {
        statData = data.target;
    } else if (id == "currentStreak") {
        statData = data.streak;
    } else {
        statData = data.unit;
        if (statData == "Weekly") {
            statData = "Weeks"
        } else {
            statData = "Days"
        };
    };

    if (statData == "") {
      statData = 0
    }
    statElement.innerHTML = statData;
}
