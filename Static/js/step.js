function setTable(stepId) {
    data = $.ajax({ url: "/API/GetStep?stepId=" + stepId, async: false }).responseJSON;
    $("#step-title").text(data['title']);
    for (var i = 0; i < data['problemList'].length; i++) {
        var proData = "<tr>";
        if (data['problemList'][i]['ZX']) {
            proData = proData + "<td rowspan=\"" + data['problemList'][i]['ZX_len'] + "\">" + data['problemList'][i]['ZX'] + "</td>";
        }
        if (data['problemList'][i]['ZT']) {
            proData = proData + "<td rowspan=\"" + data['problemList'][i]['ZT_len'] + "\">" + data['problemList'][i]['ZT'] + "</td>";
        }
        if (data['source'] == 'SDUT')
            Url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Index/problemdetail/pid/' + data['problemList'][i]['problem'] + '.html';
        else if (data['source'] == 'POJ')
            Url = 'http://poj.org/problem?id=' + data['problemList'][i]['problem'];
        else if (data['source'] == 'HDU')
            Url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + data['problemList'][i]['problem'];
        proData = proData + "<td><a href=\"" + Url + "\" target=\"_blank\" title=\"" + data['problemList'][i]['title'] + "\">" + data['source'] + " " + data['problemList'][i]['problem'] + "</a></td>";
        $("#problem-list").append(proData + "</tr>");
        $("#problem-status").append("<tr id=\"problem-" + i + "\"></tr>")
    }
    allProblemCount = data.problemList.length;
    for (var i = 0; i < data['userList'].length; i++) {
        var userData = "<th>\
        <div><a href=\"/user/?source=" + data['source'] + "&userName=" + data['userList'][i]['userName'] + "\" target=\"_blank\">" + data['userList'][i]["name"] + "<br>" + data['userList'][i]['class'] + "<p>" + data['userList'][i]['count'] + "题/" + allProblemCount + "题</p></a></div>\
        <div class=\"progress\">\
        <div id=\"user-" + i + "\" class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\"0\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>\
        </div>\
        </th>";
        $("#user-list").append(userData);
    }
}

function setStatusTimeout(id, time) {
    $("#problem-" + id).append(time);
}

function setStatus() {
    thisTime = new Date();
    stepStatus = data['data'];
    for (var i = 0; i < data['userList'].length; i++) {
        for (var j = 0; j < data['problemList'].length; j++) {
            var Time = stepStatus[data['userList'][i]['userName']][data['problemList'][j]['problem']];
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
            setTimeout("setStatusTimeout('" + j + "', '" + sTime + "')", 1);
        }
        $("#user-" + i).css('width', data['userList'][i]['count'] * 100 / allProblemCount + '%');
    }
    setTimeout('setStatistics()', 1);
}

function setStatistics() {
    $("#myModalBody").html('');
    $("#myModalBody").append('<b>总通过: ' + data['problemCount'] + '</b>&nbsp;&nbsp;|&nbsp;&nbsp;<b>完成度: ' +
        Math.ceil(Number(data['problemCount']) * 100 / data['userList'].length / data['problemList'].length) +
        '%</b>&nbsp;&nbsp;|&nbsp;&nbsp;<b>人数: ' +
        data['userList'].length + '</b>&nbsp;&nbsp;|&nbsp;&nbsp;<b>题数: ' + data['problemList'].length + '</b>');
    var uData = '<table class="table table-striped table-bordered">\
        <thead>\
          <tr>\
            <th>排名</th>\
            <th>班级</th>\
            <th>姓名</th>\
            <th>账号</th>\
            <th>题数</th>\
            <th>进度</th>\
          </tr>\
        </thead>\
        <tbody class="vertical-middle">';
    users = data['userList'];
    users.sort(cmp);
    for (var i = 0; i < users.length; i++) {
        uData = uData + '<tr><td>' + (i + 1) +
            '</td><td>' + users[i]['class'] +
            '</td><td>' + users[i]['name'] +
            '</td><td>' + users[i]['userName'] +
            '</td><td>' + users[i]['count'] + ' / ' + allProblemCount +
            '</td><td>' + Math.ceil(users[i]['count'] * 100 / allProblemCount) + ' %' +
            '</td></tr>';
    }
    $("#myModalBody").append(uData + "</tbody></table>");
}

function cmp(a, b) {
    return Number(b['count']) - Number(a['count']);
}