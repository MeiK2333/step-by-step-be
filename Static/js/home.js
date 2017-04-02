function setOrgList() {
    orgList = $.ajax({url: "/API/GetOrgList", async: false}).responseJSON;
    $("#thead").html('<th>编号</th><th>简称</th><th>组织名</th>');
    for (var i = 0; i < orgList['count']; i++) {
        $("#tbody").append('<tr><td>' + i + '</td><td>' + orgList['list'][i]['shortName'] +
         '</td><td><a href="javascript:void(0)" onclick="setStepList(\'' +
         orgList['list'][i]['id'] + '\')">' +
         orgList['list'][i]['name'] + '</a></td></tr>');
    }
}

function setStepList(id) {
    stepList = $.ajax({url: "/API/GetStepList?orgId=" + id, async: false}).responseJSON;
    $("#thead").html('<th style="width: 10%;">编号</th><th style="width: 25%;">计划名称</th>\
            <th style="width: 20%;">来源</th><th style="width: 20%;">人数</th>\
            <th style="width: 20%;">题数</th>');
    $("#tbody").html('');
    for (var i = 0; i < stepList['count']; i++) {
        $("#tbody").append('<tr><td>' + i + '</td><td style="text-align: left;">\
        <a target="_blank" href="/step/' + stepList['list'][i]['id'] + '">' + stepList['list'][i]['title'] + '</a></td>\
              <td>' + stepList['list'][i]['source'] + '</td>\
              <td>' + stepList['list'][i]['userCount'] + '</td>\
              <td>' + stepList['list'][i]['problemCount'] + '</td></tr>');
    }
}

$(document).ready(function() {
    setOrgList();
});