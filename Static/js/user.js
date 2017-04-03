function setStepList(stepId) {
    var data = $.ajax({ url: '/API/GetUserStep?stepId=' + stepId + '&userName=' + userName, async: false }).responseJSON;
    $("#step-list").append('<li role="presentation"><a href="#stepId-' + stepId +
        '" id="stepId-' + stepId + '-tab" role="tab" data-toggle="tab" aria-controls="stepId-' +
        stepId + '">' + data['title'] + '</a></li>');
    var content = '<div role="tabpanel" class="tab-pane fade" id="stepId-' + stepId +
        '" aria-labelledBy="stepId-' + stepId + '-tab">\
                        <table class="table table-bordered">\
                            <thead>\
                                <tr>\
                                    <th style="width: 20%;">专项</th>\
                                    <th style="width: 40%;">专题</th>\
                                    <th style="width: 15%;">题目</th>\
                                    <th style="width: 25%;">完成状态</th>\
                                </tr>\
                            </thead>\
                            <tbody>';
    var Url;
    for (var i = 0; i < data['problemList'].length; i++) {
        var problem = data['problemList'][i]['problem'];
        content = content + "<tr>";
        if (data['problemList'][i]['ZX']) {
            content = content + "<td rowspan=\"" + data['problemList'][i]['ZX_len'] + "\">" + data['problemList'][i]['ZX'] + "</td>";
        }
        if (data['problemList'][i]['ZT']) {
            content = content + "<td rowspan=\"" + data['problemList'][i]['ZT_len'] + "\">" + data['problemList'][i]['ZT'] + "</td>";
        }
        if (source == 'SDUT')
            Url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Index/problemdetail/pid/' + problem + '.html';
        else if (source == 'POJ')
            Url = 'http://poj.org/problem?id=' + problem;
        else if (source == 'HDU')
            Url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + problem;
        content = content + "<td><a href=\"" + Url + "\" target=\"_blank\">" + source + " " + problem + "</a></td>";
        thisTime = new Date();
        var Time = data['data'][problem];
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
        content = content + sTime;
    }
    content = content + '</tbody></table></div>';
    $("#step-content").append(content);
}

function setInfo() {
    var data = $.ajax({ url: '/API/GetUserStepList?source=' + source + '&userName=' + userName, async: false }).responseJSON;
    if (data['status']) {
        $("#user-info").html('<h2>' + userName + '</h2><h5>来源: ' + source + '</h5><h5>通过题数: ' + data['allAc'] + '</h5>');
        stepList = data['stepList'];
        for (var i = 0; i < stepList.length; i++) {
            setTimeout('setStepList("' + stepList[i] + '")', 1);
        }
    } else {
        alert(data['msg']);
    }
}

$(document).ready(function () {
    source = $("#user-source").val();
    userName = $("#user-userName").val();
    setTimeout('setInfo()', 1);
});