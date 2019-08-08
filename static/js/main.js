function login1(){
    document.getElementById("login1").style.display="block";
    document.getElementById("login2").style.display="none";
}
function login2() {
    document.getElementById("login1").style.display="none";
    document.getElementById("login2").style.display="block";
}

//页面加载后设置每隔一段时间自动执行某函数。
window.onload = function () {
    setInterval("func()",4000)
}
var i = 1;
function func() {
    if (i==3){
    i=0;
}
    i++;
    document.getElementById("img").src="../static/img/image"+i+".jpg";
}
function usertip() {
    document.getElementById("usertip").innerHTML=" *仅字母、数字、下划线";
}
function pwdtip() {
    document.getElementById("pwdtip").innerHTML=" *请为你的新邮箱设置密码";
}
function repwdtip() {
    document.getElementById("repwdtip").innerHTML=" *请再次输入设置的密码";
}
function phonetip() {
    document.getElementById("phonetip").innerHTML=" *手机号码用于找回密码";
}
function checkuser() {
    var u = document.getElementById("u").value;
    if (u===''){
        document.getElementById("usertip").innerHTML=" *用户名不能为空";
    }
}
function checkpwd() {
    var p = document.getElementById("p").value;
    if (p.length<6){
        document.getElementById("pwdtip").innerHTML=" *密码不能少与6位";
    }
}
function recheckpwd() {
    var p = document.getElementById("p").value;
    var r = document.getElementById("r").value;
    if ( p != r ){
        document.getElementById("repwdtip").innerHTML=" *两次输入密码不一致";
    }
    else if (p != '')
        document.getElementById("repwdtip").innerHTML=" *密码一致，请牢记密码";
}
function checkphone() {
    var phone = document.getElementById("phone").value;
    if (phone.length != 11){
        document.getElementById("phonetip").innerHTML=" *手机号码不符合要求";
    }
}


function savedraft() {
    document.getElementById("writeemail").action="/draft/add/";
}