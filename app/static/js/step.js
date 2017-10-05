function setTable(name, sort_id) {
    data = $.ajax({ url: "/api/plan/data/" + name + '/' + sort_id + '/', async: false }).responseJSON;
    $("#step-title").text(data['name']);
    var rewrite_cnt;
    var zx_cnt = -1;
    for (var i = 0; i < data['plan_body'].length; i++) {
        var proData = "<tr>";
        if (data['plan_body'][i]['ZX']) {
            proData = proData + "<td rowspan=\"" + data['plan_body'][i]['ZX_len'] + "\">" + data['plan_body'][i]['ZX'] + '(' + data['plan_body'][i]['ZX_len'] +')' + "</td>";
            rewrite_cnt = 0;
            zx_cnt++;
        }
        if (data['plan_body'][i]['ZT']) {
            proData = proData + "<td rowspan=\"" + data['plan_body'][i]['ZT_len'] + "\">" + data['plan_body'][i]['ZT'] + '(' + data['plan_body'][i]['ZT_len'] + ')' + "</td>";
        }
        if (data['source'] == 'SDUT')
            Url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Index/problemdetail/pid/' + data['plan_body'][i]['problem'] + '.html';
        else if (data['source'] == 'POJ')
            Url = 'http://poj.org/problem?id=' + data['plan_body'][i]['problem'];
        else if (data['source'] == 'HDU')
            Url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + data['plan_body'][i]['problem'];
        else if (data['source'] == 'UVA')
            Url = 'https://vjudge.net/problem/UVA-' + data['plan_body'][i]['problem'];
        else
            Url = '#';
        proData = proData + "<td><a href=\"" + Url + "\" target=\"_blank\" title=\"" + data['plan_body'][i]['title'] + "\">" + data['source'] + " " + data['plan_body'][i]['problem'] + "</a></td>";
        $("#problem-list").append(proData + "</tr>");
        $("#problem-status").append("<tr id=\"problem-" + i + "\"></tr>")
    }
    allProblemCount = data['plan_body'].length;
    for (var i = 0; i < data['plan_user'].length; i++) {
        var userData = "<th>\
        <div><a href=\"/user/?source=" + data['source'] + "&userName=" + data['plan_user'][i]['user_name'] + "\" target=\"_blank\">" + data['plan_user'][i]["name"] + "<br>" + data['plan_user'][i]['class'] + "<p>" + data['plan_user'][i]['count'] + "题/" + allProblemCount + "题</p></a></div>\
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

var ac_cnt = {};

function setStatus() {
    thisTime = new Date();
    stepStatus = data['plan_data'];
    for (var i = 0; i < data['plan_user'].length; i++) {
        var thisUser = data['plan_user'][i]['user_name'];
        ac_cnt[thisUser] = [0, 0, 0];
        for (var j = 0; j < data['plan_body'].length; j++) {
            var Time = stepStatus[data['plan_user'][i]['user_name']][data['plan_body'][j]['problem']];
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
                    //console.log(data['plan_user'][i]['user_name']);
                    var thisUser = data['plan_user'][i]['user_name'];
                    var ctime = thisTime.getTime() - oldTime.getTime();
                    if (ctime < 1000 * 3600 * 24 * 7) {
                        ac_cnt[thisUser][0]++;
                    }
                    if (ctime < 1000 * 3600 * 24 * 14) {
                        ac_cnt[thisUser][1]++;
                    }
                    if (ctime < 1000 * 3600 * 24 * 30) {
                        ac_cnt[thisUser][2]++;
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
        $("#user-" + i).css('width', data['plan_user'][i]['count'] * 100 / allProblemCount + '%');
    }
    setTimeout('setStatistics()', 1);
}

function setStatistics() {
    $("#myModalBody").html('');
    $("#myModalBody").append('<b>人数: ' +
        data['plan_user'].length + '</b>&nbsp;&nbsp;|&nbsp;&nbsp;<b>题数: ' + data['plan_body'].length + '</b>');
    var uData = '<table class="table table-striped table-bordered" width="1080px;">\
        <thead>\
          <tr>\
            <th>排名</th>\
            <th>班级</th>\
            <th>姓名</th>\
            <th>账号</th>\
            <th>题数</th>\
            <th>近1周</th>\
            <th>近2周</th>\
            <th>近1月</th>\
            <th>进度</th>\
          </tr>\
        </thead>\
        <tbody class="vertical-middle">';
    users = data['plan_user'];
    users.sort(cmp);
    for (var i = 0; i < users.length; i++) {
        uData = uData + '<tr><td>' + (i + 1) +
            '</td><td>' + users[i]['class'] +
            '</td><td>' + users[i]['name'] +
            '</td><td>' + users[i]['user_name'] +
            '</td><td>' + users[i]['count'] + ' / ' + allProblemCount +
            '</td><td>' + ac_cnt[users[i]['user_name']][0] + 
            '</td><td>' + ac_cnt[users[i]['user_name']][1] +
            '</td><td>' + ac_cnt[users[i]['user_name']][2] +
            '</td><td>' + Math.ceil(users[i]['count'] * 100 / allProblemCount) + ' %' +
            '</td></tr>';
    }
    $("#myModalBody").append(uData + "</tbody></table>");
}

function cmp(a, b) {
    return Number(b['count']) - Number(a['count']);
}
