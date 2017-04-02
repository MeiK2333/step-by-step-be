function setStepList() {
    stepList = $.ajax({ url: "/API/GetStepList?orgId=" + orgId, async: false }).responseJSON;
    $("#thead").html('<th>编号</th><th>计划名称</th><th>来源</th><th>人数</th><th>题数</th><th>操作</th>');
    $("#tbody").html("");
    for (var i = 0; i < stepList['count']; i++) {
        $("#tbody").append('<tr><td>' +
            stepList['list'][i]['id'] + '</td><td>' +
            '<a href="javascript:void(0)" onclick="rTitleModal(\'' + stepList['list'][i]['id'] + '\', \'' + stepList['list'][i]['title'] + '\')">' + stepList['list'][i]['title'] + '</a></td><td>' +
            stepList['list'][i]['source'] + '</td><td>' +
            '<a href="javascript:void(0)" onclick="userListModal(\'' + stepList['list'][i]['id'] + '\')">' + stepList['list'][i]['userCount'] + '</a></td><td>' +
            '<a href="javascript:void(0)" onclick="problemListModal(\'' + stepList['list'][i]['id'] + '\')">' + stepList['list'][i]['problemCount'] + '</a></td><td>' +
            '<a href="javascript:void(0)" onclick="del(\'' + stepList['list'][i]['id'] + '\')">删除</a></td></tr>');
    }
}

function del(id) {
    if (confirm("您确定要删除此计划吗")) {
        $.post('/API/Step/DeleteStep', { "orgId": orgId, "id": id }, function (result) {
            if (result['status']) {
                setStepList();
            }
        });
    }
}

function rTitleModal(id, title) {
    $("#myModalLabel").html('修改计划名');
    $("#myModalBody").html('<input type="text" id="rTitleInput" class="form-control" value="' + title + '">');
    $("#myModalSubmit").attr('onclick', 'rTitle("' + id + '")');
    $("#myModal").modal('show');
}

function rTitle(id) {
    var title = $("#rTitleInput").val();
    $.post('/API/Step/UpdateStep', { "orgId": orgId, "id": id, "title": title }, function (result) {
        if (result['status']) {
            setStepList();
            $("#myModal").modal('hide');
        }
    });
}

function problemListModal(id) {
    var pList = $.ajax({ url: "/API/GetStepProblem?stepId=" + id, async: false }).responseJSON;
    if (!pList['status'])
        return;
    $("#myModalLabel").html('题目列表');
    $("#myModalBody").html('');
    var proData = '<table class="table table-bordered" style="table-layout: fixed;">\
    <thead class="vertical-middle">\
    <tr class="step-header"><th>专项</th><th>专题</th><th>题目</th></tr></thead><tbody>';
    for (var i = 0; i < pList['problemList'].length; i++) {
        proData = proData + '<tr>';
        if (pList['problemList'][i]['ZX']) {
            proData = proData + "<td rowspan=\"" + pList['problemList'][i]['ZX_len'] + "\">" + pList['problemList'][i]['ZX'] + "</td>";
        }
        if (pList['problemList'][i]['ZT']) {
            proData = proData + "<td rowspan=\"" + pList['problemList'][i]['ZT_len'] + "\">" + pList['problemList'][i]['ZT'] + "</td>";
        }
        proData = proData + "<td>" + pList['problemList'][i]['problem'] + "</td></tr>";
    }
    $("#myModalBody").append(proData + "</tbody></table>");
    $("#myModalSubmit").attr('onclick', '$("#upFile").click()');
    $("#upFile").attr('onchange', 'upProblemExcel("' + id + '")');
    $("#myModal").modal('show');
}

function userListModal(stepId) {
    var uList = $.ajax({ url: "/API/GetStepUser?stepId=" + stepId, async: false }).responseJSON;
    if (!uList['status'])
        return;
    $("#myModalLabel").html('人员列表');
    $("#myModalBody").html('');
    var uData = '<table class="table table-striped table-bordered">\
        <thead>\
          <tr>\
            <th style="width: 10%;">编号</th>\
            <th style="width: 25%;">班级</th>\
            <th style="width: 25%;">姓名</th>\
            <th style="width: 25%;">账号</th>\
            <th style="width: 15%;">操作</th>\
          </tr>\
        </thead>\
        <tbody class="vertical-middle">';
    for (var i = 0; i < uList['userList'].length; i++) {
        uData = uData + '<tr><td>' + uList['userList'][i]['userId'] +
            '</td><td>' + uList['userList'][i]['class'] +
            '</td><td>' + uList['userList'][i]['name'] +
            '</td><td>' + uList['userList'][i]['userName'] +
            '</td><td><a href="javascript:void(0)" onclick="delUser(\'' + stepId + "', '" + uList['userList'][i]['userName'] + "', '" + uList['userList'][i]['userId'] + '\')">' +
            '删除</a></td></tr>';
    }
    $("#myModalBody").append(uData + "</tbody></table>");
    $("#myModalBody").append('<br><div class="form-inline"><div class="pull-right">\
            <div class="input-group">\
            <input type="text" class="form-control" placeholder="班级" id="addUserClass" style="width: 150px;">\
            </div>\
            <div class="input-group">\
            <input type="text" class="form-control" placeholder="姓名" id="addUserNickName" style="width: 150px;">\
            </div>\
            <div class="input-group input-group-sm">\
            <input type="text" class="form-control" placeholder="账号" id="addUserName" style="width: 150px;">\
            <span class="input-group-btn">\
            <button class="btn btn-default" onclick="addStepUser(\'' + stepId + '\')">添加</button>\
            </span></div></div><br>');
    $("#myModal").modal('show');
}

function addStepUser(stepId) {
    var userClass = $("#addUserClass").val();
    var nickName = $("#addUserNickName").val();
    var userName = $("#addUserName").val();
    alert(userClass + nickName + userName);
}

function delUser(id, userName, userId) {
    if (confirm("您确定要删除此用户吗")) {
        $.post('/API/Step/DelStepUser', { "orgId": orgId, "id": id, "userName": userName, "userId": userId }, function (result) {
            if (result['status']) {
                $("#myModal").modal('hide');
                setStepList();
            }
        });
    }
}

function upProblemExcel(id) {
    var Data = new FormData(document.forms.namedItem('fileForm'));
    Data.append("id", id);
    Data.append("orgId", orgId);
    var xmlhttp;
    if (window.XMLHttpRequest)
        xmlhttp = new XMLHttpRequest();
    else
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            $("#myModal").modal('hide');
            setStepList();
        }
    }
    xmlhttp.open("POST", "/API/Step/UpStepExcel", true);
    xmlhttp.send(Data);
    return false;
}

$(document).ready(function () {
    orgId = $("#orgId").val();
    setStepList();
});