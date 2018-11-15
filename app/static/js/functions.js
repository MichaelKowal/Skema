var $calendar;

function loadDoc(subject, professor, check100, check200, check300, check400, checkOther) {
    subjectString = subject.options[subject.selectedIndex].text;
    profString = professor.options[professor.selectedIndex].text;
    requestURL = "http://localhost:5000/skema/data?subject=" + subjectString + "&prof=" + profString;
    if(check100.checked == true) requestURL += "&level100=true";
    if(check200.checked == true) requestURL += "&level200=true";
    if(check300.checked == true) requestURL += "&level300=true";
    if(check400.checked == true) requestURL += "&level400=true";
    if(checkOther.checked == true) requestURL += "&levelOther=true";

    var dataRequest = new XMLHttpRequest();
    dataRequest.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
            var temp = JSON.parse(this.responseText);
            var array = temp.classes;
            //This for loop takes years to run if we load the entire db. I think the renderEvent code is slow, so we need to find a way to only add one event at a time
            for(var i=0; i<10; i++)
            {
                console.log(array[i]);
                $calendar.fullCalendar('renderEvent', array[i], true);
            }
        }
    };
    dataRequest.open("GET", requestURL);
    dataRequest.send();
}

function loadCalendar() {
    $calendar = $('#calendar').fullCalendar({
        defaultView: 'agendaWeek',
        columnFormat: 'ddd',
        allDaySlot: false,
        defaultDate: '2018-01-01',
        minTime: "07:00:00",
        maxTime: "22:00:00",
        header: false,
        hiddenDays: [0],
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        themeSystem: 'bootstrap4',
        events: [],
        height: 'auto'
    });
}