/**
 * 2017-10-04
 * by MeiK
 * github: https://github.com/MeiK-h/
 */

function load_nick_name() {
    // 读取域的名称
    $.get('/api/this/nick_name/', function(data, statu) {
        console.log('load nick_name...\n', data);
        $("#nick_name").text(data['nick_name']);
    })
}


function set_t_head() {
    // 生成表格头
    $("#thead").html('');
    var heads = ['序号', '计划名称', '来源', '人数', '题数', '操作'];
    var head_data = '';
    for (var i = 0; i < heads.length; i++) {
        head_data += '<td>' + heads[i] + '</td>';
    }
    $("#thead").html(head_data);
}

function by_sort_id(a, b) {
    return a.sort_id - b.sort_id;
}

function set_t_body(data) {
    // 将计划列表显示在页面上
    sorted_data = data.sort(by_sort_id);
    var body_data = '';
    for (var i = 0; i < sorted_data.length; i++) {
        var this_data = sorted_data[i];
        var tr_data = '<tr>' +
        '<td>' + this_data['sort_id'] + '</td>' +
        '<td>' +
            '<a href="javascript:void(0)" onclick="RE_plan_name_modal(' +
            this_data['sort_id'] + ',\'' +
            this_data['name']  + '\')">' +
            this_data['name'] + '</a></td>' +
        '<td>' + this_data['source'] + '</td>' +
        '<td>' +
            '<a href="javascript:void(0)" onclick="user_list_modal(' +
            this_data['sort_id'] + ',\'' +
            this_data['source']  + '\')">' +
            this_data['plan_user_cnt'] + '</a></td>' +
        '<td>' +
            '<a href="javascript:void(0)" onclick="body_list_modal(' +
            this_data['sort_id'] + ',\'' +
            this_data['source']  + '\')">' + 
            this_data['plan_body_cnt'] + '</a></td>' +
        '<td>' + '<a href="javascript:void(0)" onclick="plan_up(' + this_data['sort_id'] + ')"> 上移 </a>' +
            '<a href="javascript:void(0)" onclick="plan_down(' + this_data['sort_id'] + ')"> 下移 </a>' +
            '<a href="javascript:void(0)" onclick="plan_delete(' + this_data['sort_id'] + ')"> 删除 </a>' + '</td>' +
        '</tr>';
        body_data += tr_data;
    }
    $("#tbody").html(body_data);
}

function load_t_body() {
    // 读取计划列表
    $.get('/api/this/plan_list/', function(data, statu) {
        console.log('load plans...\n', data);
        set_t_body(data);
    })
}


function setup_csrf() {
    // 设置CSRF
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
}

function init() {
    setup_csrf();
    load_nick_name();
    set_t_head();
    load_t_body();
}

$(document).ready(function () {
    init();
})

function change_plan_sort_id(sort_id, pos) {
    // 修改计划的sort_id
    $.post('/api/this/plan_pos/', data={'sort_id': sort_id, 'pos': pos}, function(data, statu) {
        console.log('change sort_id ' + sort_id + ' to ' + pos + '...\n', data);
        load_t_body();
    })
}
function plan_up(sort_id) {
    change_plan_sort_id(sort_id, sort_id - 1);
}
function plan_down(sort_id) {
    change_plan_sort_id(sort_id, sort_id + 1);
}

function plan_delete(sort_id) {
    // 删除指定的计划
    if (!confirm('您确定要删除此计划吗？')) {
        return;
    }
    $.ajax({
        url: '/api/this/plan/',
        type: 'DELETE',
        data: {'sort_id': sort_id},
        success: function(data, statu) {
            console.log('delete sort_id...\n', data);
            load_t_body();
        }
    });
}

function RE_plan_name_modal(sort_id, old_name) {
    // 显示修改计划名称的模态框
    $("#myModalLabel").html('修改标题');
    $("#myModalBody").html('<input type="text" id="old_name" class="form-control" value="' + old_name + '">');
    $("#myModalSubmit").attr('onclick', 'RE_plan_name("' + sort_id + '")');
    $("#myModal").modal('show');
}
function RE_plan_name(sort_id) {
    // 修改计划名称
    var name = $("#old_name").val();
    $.post('/api/this/plan/name/', { "sort_id": sort_id, "name": name }, function (data, statu) {
        $("#myModal").modal('hide');
        load_t_body();
    });
}

function RE_nick_name_modal() {
    // 显示修改域的名称的模态框
    $("#myModalLabel").html('修改域');
    $("#myModalBody").html('<input type="text" id="old_name" class="form-control" value="' + $("#nick_name").text() + '">');
    $("#myModalSubmit").attr('onclick', 'RE_nick_name()');
    $("#myModal").modal('show');
}
function RE_nick_name() {
    // 更新域的名称
    var nick_name = $("#old_name").val();
    $.post('/api/this/nick_name/', data={'nick_name': nick_name}, function(data, statu) {
        $("#myModal").modal('hide');
        console.log('update nick_name to ' + nick_name + '...\n', data);
        $("#nick_name").text(data['nick_name']);
    })
}

function new_plan_modal() {
    // 显示新建计划的模态框
    $("#myModalLabel").html('新建计划');
    var modal_body = '<input type="text" id="new_plan_name" class="form-control new-plan-input" placeholder="计划名">' +
    '<select class="form-control new-plan-select" id="new_plan_source">';
    for (var i = 0; i < sources.length; i++) {
        modal_body += '<option value="' + sources[i] + '">' + sources[i] + '</option>';
    }
    modal_body += '</select>';
    $("#myModalBody").html(modal_body);
    $("#myModalSubmit").attr('onclick', 'new_plan()');
    $("#myModal").modal('show');
}

function new_plan() {
    // 新建计划
    var name = $("#new_plan_name").val();
    var source = $("#new_plan_source").val();
    if (name == "") {
        return;
    }
    $.post('/api/this/plan_list/', data={'name': name, 'source': source}, function(data, statu) {
        $("#myModal").modal('hide');
        console.log('new plan...\n', data);
        load_t_body();
    })
}

function strToJson(str) { 
    var json = eval('(' + str + ')');
    return json; 
}
function update_excel(func, sort_id, source) {
    var Data = new FormData(document.forms.namedItem('fileForm'));
    var xmlhttp;
    if (window.XMLHttpRequest)
        xmlhttp = new XMLHttpRequest();
    else
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var data = strToJson(xmlhttp.responseText);
            console.log(data);
            func(sort_id, source, data);
        }
    }
    xmlhttp.open("POST", "/util/parser_excel/", true);
    xmlhttp.send(Data);
    return false;
}

function user_list_modal(sort_id, source) {
    // 显示某计划的用户列表模态框
    $.get('/api/this/plan/user_list/', data={'sort_id': sort_id}, function(data, statu) {
        $("#myModalLabel").html('用户列表');
        var table_body = '<table class="table table-striped table-bordered"><thead><tr>' +
        '<th>ID</th><th>班级</th><th>姓名</th><th>账号</th><th>操作</th></tr></thead>' +
        '<tbody class="vertical-middle">';
        for (var i = 0; i < data.length; i++) {
            table_body += '<tr><td>' +
            data[i]['id'] + '</td><td>' +
            data[i]['class'] + '</td><td>' +
            data[i]['name'] + '</td><td>' +
            data[i]['user_name'] + '</td><td><a href="javascript:void(0)" onclick="delete_user(' +
            sort_id + ',\'' + data[i]['id'] + '\', \'' + source + '\')">删除</a></td></tr>';
        }
        table_body += '</tbody></table>';
        $("#myModalBody").html(table_body);
        $("#myModalSubmit").attr('onclick', '$("#upFile").click()');
        $("#upFile").attr('onchange', 'upload_user_excel("' + sort_id + '", "' + source + '")');
        $("#myModal").modal('show');
    })
}
function upload_user_excel(sort_id, source) {
    update_excel(update_user_list_modal, sort_id, source);
}
function update_user_list_modal(sort_id, source, data) {
    // 显示某计划的用户验证列表
    $("#myModalLabel").html('验证用户');
    var id_col = 0;
    var class_col = 1;
    var name_col = 2;
    var user_name_col = -1;
    for (var i = 0; i < data.cols; i++) {
        if (source === data['data'][0][i]) {
            user_name_col = i;
        }
    }
    if (user_name_col === -1) {
        alert('对应账号未找到');
        return;
    }
    var table_body = '<table class="table table-striped table-bordered"><thead><tr>' +
        '<th>ID</th><th>班级</th><th>姓名</th><th>账号</th><th>状态</th></tr></thead>' +
        '<tbody class="vertical-middle" id="check_tbody">';
    for (var i = 1; i < data.rows; i++) {
        if (data['data'][i][user_name_col] === '') {
            continue;
        }
        table_body += '<tr id="check_tr_' + i + '"><td>' +
        data['data'][i][id_col] + '</td><td>' +
        data['data'][i][class_col] + '</td><td>' +
        data['data'][i][name_col] + '</td><td>' +
        data['data'][i][user_name_col] + '</td><td><font color="#8b8b8b">未校验</font></td></tr>';
    }
    table_body += '</tbody></table>';
    $("#myModalBody").html(table_body);
    $("#myModalSubmit").attr('onclick', 'alert("弄啥嘞")');
    $("#myModal").modal('show');
    check_start(sort_id, source);
}
function check_start(sort_id, source) {
    // 验证用户是否存在
    var users = $("#check_tbody").find("tr");
    check_next(sort_id, source, 0, users.length);
}
function check_next(sort_id, source, i, l) {
    console.log(i, l);
    if (i >= l) {
        load_t_body();
        return;
    }
    var users = $("#check_tbody").find("tr");
    var this_user = users.eq(i).children();
    var id = this_user.eq(0).text();
    var class_ = this_user.eq(1).text();
    var name = this_user.eq(2).text();
    var user_name = this_user.eq(3).text();
    var up_data = {
        'sort_id': sort_id,
        'source': source,
        'user_id': id,
        'class': class_,
        'name': name,
        'user_name': user_name,
    }
    $.post('/util/check_user/', data=up_data, function(data, statu) {
        if (data['exist']) {
            console.log(data);
            this_user.eq(4).html('<font color="green">验证通过</font>');

            $.post('/api/this/plan/user_list/', data=up_data, function(data, statu) {
                console.log(data);
                if (statu['code'] == 0) {
                    this_user.eq(4).html('<font color="red">提交失败</font>');
                } else {
                    this_user.eq(4).html('<font color="green">提交通过</font>');
                }
            })

            setTimeout('check_next(' + sort_id + ',' +
                '"' + source + '",' + '' + (i + 1) + ',' + l + ')', 10);
        } else {
            this_user.eq(4).html('<font color="red">验证失败</font>');
            setTimeout('check_next(' + sort_id + ',' +
                '"' + source + '",' + '' + (i + 1) + ',' + l + ')', 10);
        }
    })
}
var delete_query_flag = true;
function delete_user(sort_id, user_id, source) {
    // 从某计划中删除一个用户
    if (delete_query_flag && confirm('您确定要删除 ' + user_id + ' 吗？')) {
        $.ajax({
            url: '/api/this/plan/user_list/',
            type: 'DELETE',
            data: {'sort_id': sort_id, 'user_id': user_id},
            success: function(data, statu) {
                console.log('delete user_id...\n', data);
                load_t_body();
                user_list_modal(sort_id, source);
            }
        });
    }
}

function body_list_modal(sort_id, source) {
    // 显示某计划的题目列表模态框
    $.get('/api/this/plan/body/', data={'sort_id': sort_id}, function(data, statu) {
        $("#myModalLabel").html('题目列表');
        console.log(data);
        var table_body = '<table class="table table-bordered" style="table-layout: fixed;">\
        <thead class="vertical-middle">\
        <tr class="step-header"><th>专题</th><th>专项</th><th>题目</th></tr></thead><tbody>';
        for (var i = 0; i < data.length; i++) {
            table_body += '<tr>';
            if (data[i]['ZX']) {
                table_body += "<td rowspan=\"" + data[i]['ZX_len'] + "\">" + data[i]['ZX'] + "</td>";
            }
            if (data[i]['ZT']) {
                table_body += "<td rowspan=\"" + data[i]['ZT_len'] + "\">" + data[i]['ZT'] + "</td>";
            }
            table_body += "<td>" + data[i]['problem'] + "</td></tr>";
        }
        table_body += '</tbody></table>';
        $("#myModalBody").html(table_body);

        $("#myModalSubmit").attr('onclick', '$("#upFile").click()');
        $("#upFile").attr('onchange', 'upload_body_excel("' + sort_id + '", "' + source + '")');
        $("#myModal").modal('show');
    })
}
function upload_body_excel(sort_id, source) {
    update_excel(update_body_list, sort_id, source);
}
function update_body_list(sort_id, source, data) {
    // 上传计划主体
    if (data['cols'] < 3) {
        alert('这个表不对吧大兄弟');
        return;
    }
    var up_data = [];
    var zt_len = 0;
    var zx_len = 0;
    for (var i = data['data'].length - 1; i >= 0; i--) {
        var d = {'problem': '' + data['data'][i][2]};
        zx_len++;
        zt_len++;
        if (data['data'][i][0] !== '') {
            d['ZX'] = '' + data['data'][i][0];
            d['ZX_len'] = zx_len;
            zx_len = 0;
        }
        if (data['data'][i][1] !== '') {
            d['ZT'] = '' + data['data'][i][1];
            d['ZT_len'] = zt_len;
            zt_len = 0;
        }
        up_data[up_data.length] = d;
    }
    up_data.reverse()
    up_data_str = JSON.stringify(up_data);
    console.log(up_data_str);
    $.post('/api/this/plan/body/', data={'sort_id': sort_id, 'plan_body': up_data_str}, function(data, statu) {
        body_list_modal(sort_id, source);
    })
}