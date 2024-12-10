

$.ajax({ 
    method: "GET", 
    url: userStreakEndpoint,
    success: function(data) {
        console.log("data ", data);
        if (data.target > 0) {
            console.log("target " + data.target);
            displayStreakData(data, 'currentApplications');
            displayStreakData(data, 'targetAmount');
            displayStreakData(data, 'currentStreak');

        }
      
    }, 
    error: function(error_data) { 
      console.log(error_data); 
    } 
  });
  function displayStreakData(data, id) {
    console.log("id " + id);
    var statData = "";
    var statElement = document.getElementById(id);
    if (id == "currentApplications") {
        statData = data.current_applications;
    } else if (id == "targetAmount") {
        statData = data.target;
    } else {
        statData = data.streak;
    };

    if (statData == "") {
      statData = 0
    }
    console.log("statData " + statData);
    statElement.innerHTML = statData;
}
