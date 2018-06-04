//window.onload = function(){
   //setTimeout("setInterval(getTaskStatus,50000)", 3000);
//}
function refreshAmbariStatus(){
    setTimeout("setInterval(getAmbariStatus,50000)", 3000);
}
function getAmbariStatus() {
    var taskid = document.getElementById("taskid").innerText;
    $.ajax({
            type: "GET",
            dataType: "json",//预期服务器返回的数据类型
            url: "/ambari_status_query" ,//url
            data: {"taskid":taskid, },
            success: function (result) {
                console.log(result);
                document.getElementById("server_status").innerText = result['server_status'];
                document.getElementById("agents_status").innerText = result['agents_status'];
            },
            error : function() {
                alert("未知异常！");
            }
    });
}
function queryHdpLog(){
    var taskid = document.getElementById("taskid").innerText;
    $.ajax({
        type: "GET",
        dataType: "json",//预期服务器返回的数据类型
        url: "/query_hdp_log" ,//url
        data: {"taskid":taskid,},
        success: function (result) {
            console.log(result);
            document.getElementById("log_text").innerText = result['log'];
        },
        error : function() {
            document.getElementById("log_text").innerText = "fail to load hdp log";
        }
    });
}
function queryServerLog(){
    var taskid = document.getElementById("taskid").innerText;
    $.ajax({
        type: "GET",
        dataType: "json",//预期服务器返回的数据类型
        url: "/query_server_log" ,//url
        data: {"taskid":taskid, },
        success: function (result) {
            console.log(result);
            document.getElementById("log_text").innerText = result['log'];
        },
        error : function() {
            document.getElementById("log_text").innerText = "fail to load server log";
        }
    });
}
function queryAgentsLog(){
    var taskid = document.getElementById("taskid").innerText;
    $.ajax({
        type: "GET",
        dataType: "json",//预期服务器返回的数据类型
        url: "/query_agents_log" ,//url
        data: {"taskid":taskid, },
        success: function (result) {
            console.log(result);
            document.getElementById("log_text").innerText = result['log'];
        },
        error : function() {
            document.getElementById("log_text").innerText = "fail to load agents log";
        }
    });
}
function queryAgentLog(ip){
    var taskid = document.getElementById("taskid").innerText;
    $.ajax({
        type: "GET",
        dataType: "json",//预期服务器返回的数据类型
        url: "/query_agent_log" ,//url
        data: {"taskid":taskid, "ip":ip},
        success: function (result) {
            console.log(result);
            document.getElementById("log_text").innerText = result['log'];
        },
        error : function() {
            document.getElementById("log_text").innerText = "fail to load agent log";
        }
    });
}