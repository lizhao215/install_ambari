//window.onload = function(){
   //setTimeout("setInterval(getTaskStatus,50000)", 3000);
//}
function validate() {
    if (confirm("提交表单?")) {
      return true;
    } else {
      return false;
    }
   }
function isValidIP(ip) {
    var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
    return reg.test(ip);
}
function trim(str){
    return str.replace(/(^\s*)|(\s*$)/g, "");
}
function checkHosts(hosts, splitReg , num){
    // alert(hosts);
    hostList = hosts.split("\n")
    for (i in hostList){
        // alert("line trim: " + hostList[i].trim());
        host=hostList[i].trim().split(splitReg)
        if ( ! isValidIP(host[0]) || host.length != num){
            alert("hosts lineNum:" + i + " '" + hostList[i] + "' is invalid !!");
            return false;
        }
    }
    return true;
}
function checkHostPassword(host, password){
    $.ajax({
        type: "GET",
        dataType: "json",  //预期服务器返回的数据类型
        url: "/check_host_password" ,//url
        data: {"host":host,"password":password},
        success: function (data) {
            console.log(result);
            if (data['result'] == "true"){
                return true;
            }else{
                return false;
            }
        },
        error : function() {
            alert("未知异常！");
        }
	});
}
function submitForm() {
    if (validate()) {
        var controlip = document.getElementById("controlip").value;
        var controlpwd = document.getElementById("controlpwd").value;
        var serverip = document.getElementById("serverip").value;
        var hosts = document.getElementById("hosts").value;
        if  ( ! isValidIP(controlip)){
            alert("controlip is invalid !!!");
            return false;
        }else if(! isValidIP(serverip)){
            alert("serverip is invalid !!!");
            return false;
        }else if (! checkHosts(hosts, " ", 3)){
            return false;
        }
        return false;
        $.ajax({
			type: "GET",
			dataType: "json",  //预期服务器返回的数据类型
			url: "/ambari_install_submit" ,//url
			data: {"serverip":serverip,"controlip":controlip,"controlpwd":controlpwd,"hosts":hosts},
			success: function (result) {
				console.log(result);
				window.location.href="/ambari_install_progress?taskid=" + result['taskid'];
                refreshAmbariStatus();
			},
			error : function() {
				alert("未知异常！");
			}
		});
    }
}
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