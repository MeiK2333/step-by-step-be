//显示所有的计划列表，添加操作属性
function setStepList() {
    stepList = $.ajax({ url: "/API/GetStepList?orgId=" + orgId, async: false }).responseJSON;
    if (!stepList['status']) {
        alert(stepList['msg']);
    }
    $("#thead").html('<th>编号</th><th>计划名称</th><th>来源</th><th>人数</th><th>题数</th><th>操作</th>');
    $("#tbody").html("");
    for (var i = 0; i < stepList['count']; i++) {
        $("#tbody").append('<tr><td>' +
            stepList['list'][i]['id'] + '</td><td>' +
            '<a href="javascript:void(0)" onclick="rTitleModal(\'' + stepList['list'][i]['id'] + '\', \'' + stepList['list'][i]['title'] + '\')">' + stepList['list'][i]['title'] + '</a></td><td>' +
            stepList['list'][i]['source'] + '</td><td>' +
            '<a href="javascript:void(0)" onclick="userListModal(\'' + stepList['list'][i]['id'] + "', '" + stepList['list'][i]['source'] + '\')">' + stepList['list'][i]['userCount'] + '</a></td><td>' +
            '<a href="javascript:void(0)" onclick="problemListModal(\'' + stepList['list'][i]['id'] + '\')">' + stepList['list'][i]['problemCount'] + '</a></td><td>' +
            '<a href="javascript:void(0)" onclick="del(\'' + stepList['list'][i]['id'] + '\')">删除</a></td></tr>');
    }
}

//删除某计划
function del(id) {
    if (confirm("您确定要删除此计划吗")) {
        $.post('/API/Step/DeleteStep', { "orgId": orgId, "id": id }, function (result) {
            if (result['status']) {
                setStepList();
            } else {
                alert(result['msg']);
            }
        });
    }
}

//显示修改计划名的模态框
function rTitleModal(id, title) {
    $("#myModalLabel").html('修改计划名');
    $("#myModalBody").html('<input type="text" id="rTitleInput" class="form-control" value="' + title + '">');
    $("#myModalSubmit").attr('onclick', 'rTitle("' + id + '")');
    $("#myModal").modal('show');
}

//修改计划名
function rTitle(id) {
    var title = $("#rTitleInput").val();
    $.post('/API/Step/UpdateStep', { "orgId": orgId, "id": id, "title": title }, function (result) {
        if (result['status']) {
            $("#myModal").modal('hide');
            setStepList();
        } else {
            alert(result['msg']);
        }
    });
}

//显示计划题目列表
function problemListModal(stepId) {
    var pList = $.ajax({ url: "/API/GetStepProblem?stepId=" + stepId, async: false }).responseJSON;
    if (!pList['status']) {
        alert(pList['msg']);
        return;
    }
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
    $("#upFile").attr('onchange', 'upProblemExcel("' + stepId + '")');
    $("#myModal").modal('show');
}

//显示计划用户列表
function userListModal(stepId, source) {
    var uList = $.ajax({ url: "/API/GetStepUser?stepId=" + stepId, async: false }).responseJSON;
    if (!uList['status']) {
        alert(uList['msg']);
        return;
    }
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
            <button class="btn btn-default" onclick="checkStepUser(\'' + stepId + "', '" + source + '\')">添加</button>\
            </span></div></div><br>');
    $("#myModalSubmit").attr('onclick', '$("#upFile").click()');
    $("#upFile").attr('onchange', 'upUserExcel("' + stepId + '")');
    $("#myModal").modal('show');
}

//检查添加用户是否存在
function checkStepUser(stepId, source) {
    var userClass = $("#addUserClass").val();
    var nickName = $("#addUserNickName").val();
    var userName = $("#addUserName").val();
    if (!(userClass && nickName && nickName)) {
        alert('请填写全部信息');
        return;
    }
    var status = $.ajax({ url: "/API/CheckUser?source=" + source + "&userName=" + userName, async: false }).responseJSON;
    if (status['status']) {
        addStepUser(stepId, userClass, nickName, userName);
    } else {
        alert(status['msg']);
    }
}

//为计划添加用户
function addStepUser(stepId, userClass, nickName, userName) {
    var dataJson = {
        "orgId": orgId,
        "id": stepId,
        "userName": userName,
        "nickName": nickName,
        "class": userClass
    };
    $.post('/API/Step/AddStepUser', dataJson, function (result) {
        if (result['status']) {
            $("#myModal").modal('hide');
            setStepList();
        } else {
            alert(result['msg']);
        }
    });
}

//为计划删除用户
function delUser(id, userName, userId) {
    if (confirm("您确定要删除此用户吗")) {
        $.post('/API/Step/DelStepUser', { "orgId": orgId, "id": id, "userName": userName, "userId": userId }, function (result) {
            if (result['status']) {
                $("#myModal").modal('hide');
                setStepList();
            } else {
                alert(result['msg']);
            }
        });
    }
}

//为计划上传Excel格式的题目
function upProblemExcel(stepId) {
    var Data = new FormData(document.forms.namedItem('fileForm'));
    Data.append("id", stepId);
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

//上传Excel格式的用户
function upUserExcel(stepId) {
    var Data = new FormData(document.forms.namedItem('fileForm'));
    Data.append("id", stepId);
    Data.append("orgId", orgId);
    var xmlhttp;
    if (window.XMLHttpRequest)
        xmlhttp = new XMLHttpRequest();
    else
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            allUserModel(xmlhttp.responseText);
        }
    }
    xmlhttp.open("POST", "/API/Step/UpUserExcel", true);
    xmlhttp.send(Data);
    return false;
}

//显示Excel解析的用户数据
function allUserModel(response) {
    var uList = JSON.parse(response);
    $("#myModalLabel").html('人员列表');
    $("#myModalBody").html('');
    var uData = '<table class="table table-striped table-bordered">\
        <thead>\
          <tr>\
            <th>班级</th>\
            <th>姓名</th>\
            <th>账号</th>\
            <th>状态</th>\
          </tr>\
        </thead>\
        <tbody class="vertical-middle">';
    var i;
    for (i = 0; i < uList['userList'].length; i++) {
        uData = uData + '<tr id="jy-' + i + '"><td>' +
            uList['userList'][i]['class'] +
            '</td><td>' + uList['userList'][i]['name'] +
            '</td><td>' + uList['userList'][i]['userName'] +
            '</td><td>未校验</td></tr>';
    }
    $("#myModalBody").append(uData + "</tbody></table>");
    $("#myModalSubmit").attr('onclick', 'alert("请等待校验完成")');
    var source = uList['data']['source'];
    var stepId = uList['data']['id'];
    setTimeout("allUserCheck(0, " + i + ", '" + source + "', '" + stepId + "')", 1000);
}

//批量验证列表内的用户
function allUserCheck(l, r, source, stepId) {
    if (l >= r) {
        $("#myModal").modal('hide');
        setStepList();
        return;
    }
    var s = $("#jy-" + l).children();
    var userClass = s[0].innerText;
    var nickName = s[1].innerText;
    var userName = s[2].innerText;
    if (!(userClass && nickName && nickName)) {
        s[3].innerHTML = '<span style="color: red">信息不全</span>';
        setTimeout("allUserCheck(" + (Number(l) + 1) + ", " + r + ", '" + source + "', '" + stepId + "')", 100);
        return;
    }
    var status = $.ajax({ url: "/API/CheckUser?source=" + source + "&userName=" + userName, async: false }).responseJSON;
    if (status['status']) {
        if (status['uid']) {
            s[2].innerText = status['uid'];
            userName = status['uid'];
        }
        var dataJson = {
            "orgId": orgId,
            "id": stepId,
            "userName": userName,
            "nickName": nickName,
            "class": userClass
        };
        $.post('/API/Step/AddStepUser', dataJson, function (result) {
            if (result['status']) {
                s[3].innerHTML = '<span style="color: green">校验通过</span>';
                setTimeout("allUserCheck(" + (Number(l) + 1) + ", " + r + ", '" + source + "', '" + stepId + "')", 100);
                return;
            } else {
                s[3].innerHTML = '<span style="color: red">' + result['msg'] + '</span>';
                setTimeout("allUserCheck(" + (Number(l) + 1) + ", " + r + ", '" + source + "', '" + stepId + "')", 100);
                return;
            }
        });
    } else {
        s[3].innerHTML = '<span style="color: red">' + status['msg'] + '</span>';
        setTimeout("allUserCheck(" + (Number(l) + 1) + ", " + r + ", '" + source + "', '" + stepId + "')", 100);
        return;
    }
}

//新建计划
function createStep() {
    var source = $("#createStepSource").val();
    var title = $("#createStepTitle").val();
    $.post('/API/Step/CreateStep', {"orgId": orgId, "title": title, "source": source}, function(result){
       if (result['status']) {
           setStepList();
       } else {
           alert(result['msg']);
       }
    });
}

function logout() {
    $.ajax({ url: "/API/Logout", async: false });
    location.reload(true);
}

$(document).ready(function () {
    orgId = $("#orgId").val();
    setStepList();
});