function setTable() {
    data = $.ajax({url: "step1.json", async: false}).responseJSON;
    $("#step-title").text(data['title']);
    for (var i = 0; i < data['problemList'].length; i++) {
        var proData = "<tr>";
        if (data['problemList'][i]['ZX']) {
            proData = proData + "<td rowspan=\"" + data['problemList'][i]['ZX_len'] + "\">" + data['problemList'][i]['ZX'] + "</td>";
        }
        if (data['problemList'][i]['ZT']) {
            proData = proData + "<td rowspan=\"" + data['problemList'][i]['ZT_len'] + "\">" + data['problemList'][i]['ZT'] + "</td>";
        }
        proData = proData + "<td><a href=\"\" target=\"_blank\" title=\"" + data['problemList'][i]['title'] + "\">" + data['source'] + " " + data['problemList'][i]['problem'] + "</a></td>";
        $("#problem-list").append(proData + "</tr>");
        $("#problem-status").append("<tr id=\"problem-" + data['problemList'][i]['problem'] + "\"></tr>")
    }
    for (var i = 0; i < data['userList'].length; i++) {
        var userData = "<th>\
        <div><a href=\"#\">" + data['userList'][i]["name"] + "<br>" + data['userList'][i]['class'] + "<p>" + data['userList'][i]['count'] + "题/" + data['problemCount'] + "题</p></a></div>\
        <div class=\"progress\">\
        <div id=\"user-" + i + "\" class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\"0\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>\
        </div>\
        </th>";
        $("#user-list").append(userData);
    }
}

function setProgress(i) {
    $("#user-" + i).css('width', data['userList'][i]['count']*100/data['problemCount']);
}

function setStatusTimeout(id, time) {
    $("#problem-" + id).append(time);
}

function setStatus() {
    thisTime = new Date();
    stepStatus = $.ajax({url: "step1status.json", async: false}).responseJSON;
    for (var i = 0; i < data['userList'].length; i++) {
        for (var j = 0; j < data['problemList'].length; j++) {
            var Time = stepStatus['status'][data['userList'][i]['userName']][data['problemList'][j]['problem']];
            var sTime;
            if (Time) {
                if (Time.length == 10) {
                    var times = Time.split("-");
                    var oldTime = new Date(times[0], times[1] - 1, times[2]);
                    if (thisTime.getTime() - oldTime.getTime() < 1000 * 3600 * 24 * 7) {
                        sTime = "<td class=\"ac-new\">" + Time + "</td>";
                    } else {
                        sTime = "<td class=\"success\">" + Time + "</td>";
                    }
                } else {
                    var times = Time.substr(0, 10).split("-");
                    var oldTime = new Date(times[0], times[1] - 1, times[2]);
                    if (thisTime.getTime() - oldTime.getTime() < 1000 * 3600 * 24 * 7) {
                        sTime = "<td class=\"failed-new\">" + Time.substr(0, 10) + "</td>";
                    } else {
                        sTime = "<td class=\"danger\">" + Time.substr(0, 10) + "</td>";
                    }
                }
            } else {
                sTime = "<td></td>";
            }
            setTimeout("setStatusTimeout('" + data['problemList'][j]['problem'] + "', '" + sTime + "')", 1);
        }
        $("#user-" + i).css('width', data['userList'][i]['count']*100/data['problemCount'] + '%');
    }
}