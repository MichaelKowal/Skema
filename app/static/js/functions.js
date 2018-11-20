var $calendar;
var coursesInSideBar = [];

function getCoursesFromServer(subject, professor, check100, check200, check300, check400, checkOther, displayedCoursesList) {
    subjectString = subject.options[subject.selectedIndex].text;
    profString = professor.options[professor.selectedIndex].text;

    requestURL = "http://localhost:5000/data?subject=" + subjectString + "&prof=" + profString;
    if(check100.checked === true) requestURL += "&level100=true";
    if(check200.checked === true) requestURL += "&level200=true";
    if(check300.checked === true) requestURL += "&level300=true";
    if(check400.checked === true) requestURL += "&level400=true";
    if(checkOther.checked === true) requestURL += "&levelOther=true";

    var dataRequest = new XMLHttpRequest();
    dataRequest.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
            var coursesReturnedFromServer = JSON.parse(this.responseText);
            coursesInSideBar = coursesReturnedFromServer.classes;
            displayedCoursesList.innerHTML = null;
            var newDisplayedCoursesList = "";
            for(var i=0; i<coursesInSideBar.length; i++){
                newDisplayedCoursesList += "<li><a href=\"#\" onclick='addCourseToCalendar(this)'>" +
                    coursesInSideBar[i]["title"] + "</a></li>\n";
            }
            displayedCoursesList.innerHTML = newDisplayedCoursesList;
        }
    };
    dataRequest.open("GET", requestURL);
    dataRequest.send();
}

function addCourseToCalendar(courseClicked){
    var courseTitle = courseClicked.innerText;
    for(var i=0; i<coursesInSideBar.length; i++){
        if(courseTitle === coursesInSideBar[i]["title"]){
            $calendar.fullCalendar('renderEvent', coursesInSideBar[i], true)
        }
    }
}

function removeAllEvents(){
    $calendar.fullCalendar('removeEvents');
    document.getElementById("courseList").innerHTML = "";
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