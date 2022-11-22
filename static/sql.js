window.onload=function(){
    NProgress.start();
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', 'http://127.0.0.1:5000/SQL3', true);//第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
    httpRequest.send(null);//第三步：发送请求  将请求参数写在URL中
    console.log(httpRequest.responseText);
    document.getElementById("form4").innerHTML=httpRequest.responseText;
    alert('start');
}

var t = null;
t = setTimeout(time, 10); //開始运行
function time() {
    clearTimeout(t); //清除定时器
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象

    httpRequest.open('GET', 'http://127.0.0.1:5000/SQL0', false);//第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
    httpRequest.send(null);//第三步：发送请求  将请求参数写在URL中
    document.getElementById("form5").innerHTML=httpRequest.responseText;

//    httpRequest.open('GET', 'http://127.0.0.1:5000/degree', false);//第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
//    httpRequest.send(null);//第三步：发送请求  将请求参数写在URL中
//    degree = parseFloat(httpRequest.responseText);
//    if(degree==1){
//        NProgress.done();
//        document.getElementById("degree0").style.backgroundColor='#29d';
//    }
//    else
//        NProgress.set(degree);
//
//    httpRequest.open('GET', 'http://127.0.0.1:5000/bugName', false);//第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
//    httpRequest.send(null);//第三步：发送请求  将请求参数写在URL中
//    document.getElementById("Name0").value=httpRequest.responseText;
//    console.log(httpRequest.responseText);
    t = setTimeout(time, 1000);
}