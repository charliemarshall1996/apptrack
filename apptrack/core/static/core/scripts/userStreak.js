

$.ajax({ 
    method: "GET", 
    url: userDataEndpoint,
    success: function(data) {
        console.log("data ", data);
        var streakData = data.streak
        if (streakData.target > 0) {
            
            console.log("target " + streakData.target);
            displayStreakData(streakData, 'target');
            displayStreakData(streakData, 'streak');

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

    console.log("statElement " + statElement);
    if (id == "target") {
        statData = data.target_display;
    } else {
        statData = data.streak_display;
    };

    if (statData == "") {
      statData = 0
    }
    console.log("statData " + statData);
    statElement.innerHTML = statData;
}
