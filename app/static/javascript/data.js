
function Add() {

let element = document.getElementById('node');

// Vị trí 1: beforeend
element.insertAdjacentHTML("beforeend", '<td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td>');


}



function CheckMK(){
fetch('/api/check',{
    method: "post",
    body: JSON.stringify({
      "matkhau":document.getElementById("pwd").value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     alert(data.message);
     if (data.status===400)
        window.location = "/logout";
      else
        document.getElementById("LoaiBenh").id="myModal";
//     alert(data.message)
  })

}





function Checktendangki(event, minKt, maxKt) {

    event.preventDefault();

    var mess = $("#errorText");

    var username = $("#tendn").val();

    if (username == '')

    {

        $('tendn').css('background-color', 'yellow');

        mess.html(mess.html() + 'Tên đăng nhập ko được để trống ');

    } else if ((username.length > 0 && username.length < minKt) || username.length > maxKt)

    {

        $('#tendn').css('background-color', 'yellow');

        mess.html(mess.html() + 'Tên đăng nhập từ 3-10 kí tự ');

    } else mess.html(mess.html() + 'Tên đăng nhập của bạn là :' + username + '');

}

function ktrMatKhau(){

var password=document.getElementById('pwd');

if (password==null || password==""){
  alert("Vui lòng nhập mật khẩu");
  return false;
}else if(password.length<4){
  alert("Mật khẩu phải dài hơn 4 kí tự.");
  return false;
  }
}



function add_booking(){
  fetch('/api/bookschedule',{
    method: "post",
    body: JSON.stringify({
      "NgayKham":document.getElementById("NgayKham").value,
      "DVKham":document.getElementById("DVKham").value,
      "HoTen":document.getElementById("HoTen").value,
      "DiaChi": document.getElementById("DiaChi").value,
      "TrieuChung":document.getElementById("TrieuChung").value,
      "SDT": document.getElementById("sdt").value,
      "GioiTinh": document.getElementById("GioiTinh").value,
      "NamSinh": document.getElementById("NamSinh").value,

    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     if (data.status===200)
     {
       document.getElementsByClassName("error")[0].style.display="none";
       document.getElementsByClassName("success")[0].style.display="block";
      }
       else
       {
       alert(data.message);
        document.getElementsByClassName("success")[0].style.display="none";
       document.getElementsByClassName("error")[0].style.display="block";
        }
//     alert(data.message)
  })
}



function add_PK(){
  fetch('/api/lapphieukham',{
    method: "post",
    body: JSON.stringify({
      "NgayKham":document.getElementById("hvn").value,
      "TrieuChung":document.getElementById("TrieuChung").value,
      "ChuanDoanBenh":document.getElementById("LoaiBenh").value,
       "HoTen":document.getElementById("HoTen").value,

    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     if (data.status===200)
     {
       document.getElementsByClassName("error")[0].style.display="none";
       document.getElementsByClassName("success")[0].style.display="block";
      }
       else
       {
       alert(data.message);
        document.getElementsByClassName("success")[0].style.display="none";
       document.getElementsByClassName("error")[0].style.display="block";
        }
//     alert(data.message)
  })
}



function getDate() {
   var today = new Date();
   var date = today.toLocaleDateString()
   document.getElementById("hvn").value = date;
}