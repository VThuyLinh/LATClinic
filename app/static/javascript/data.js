




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




function AddThuoc() {

let element = document.getElementById('node');
let dem = element.querySelectorAll(' tr').length
let x= `<td id="abc${dem}"><input type="text" value=${dem}></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td>`

element.insertAdjacentHTML("beforeend",x);

}

function reset() {
    localStorage.clear("clickcount");
}

function laycheck(){
document.getElementById('action').onclick = function(e){
                if (this.checked){
                    alert("Bạn vừa thích freetuts.net");
                }
                else{
                    alert("Bạn vừa bỏ thích freetuts.net");
                }
            };
}

//function valueChange(event){
//  if (saveCheckbox.checked){
//    msg.innerText = 'Đã chọn Save';
//  }else{
//    msg.innerText = 'Bỏ chọn Save';
//  }
//}
//
//let saveCheckbox = document.getElementById('saveCheckbox');
//saveCheckbox.addEventListener('change', valueChange);
//let msg = document.getElementById('msg');


function getThuoctuPK(){
var str="Ban da chon thuoc:"
 var x = document.getElementsByName("thuoc");
 for (var i =0; i< x.length; i++)
 {
       if(x[i].checked == true){
            str += x[i].value + ";";
       }
 }
 console.log(str);
 }


 function RaPhieuKham(){
 var str= null;
 var x = document.getElementsByName("thuoc");
 for (var i =0; i< x.length; i++)
 {
       if(x[i].checked == true){
            str += x[i].value +";"
       }
 }
// document.getElementByName("ChuoiThuoc").value=str;
console.log(str);
 }


function getThongTin() {
 var x= document.getElementById("")
}


function hien(){
  var x = document.getElementById("bangthuoc");
  var y = document.getElementById("hsbn");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
  else{
  x.style.display = "none";
  }
}
function hienthi() {

 var y = document.getElementById("hsbn");
  if (y.style.display === "none") {
    y.style.display = "block";
  }
  else{
  y.style.display = "none";
  }
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

  function TinhTien() {
         var x= Number(document.getElementById('n1').value)
         var y = Number(document.getElementById('n2').value)
        document.getElementById('tong').value=x+y
        }

function getDate() {
   var today = new Date();
   var yyyy= today.getFullYear()
   let mm= today.getMonth()+1
   let dd = today.getDate();
   if (dd < 10) dd = '0' + dd;
    if (mm < 10) mm = '0' + mm;
   var fDate = yyyy + '/' + mm + '/' + dd;
   document.getElementById('hvn').value = fDate;

}



function getPhieuKham() {
   document.getElementById('tenthuoc').value= document.getElementById('idThuoc').value
   document.getElementById('hvn').value = date;
}



//-----------Lưu Tạm Thời------------------
function luuTamThoi(){
 let tick = document.getElementById("nodee").querySelectorAll(" input[type='checkbox']:checked")
 let a = document.getElementByName("thuoc").value

 fetch("/api/luutamthoi", {
  method: "post",
  body: JSON.stringify({
   "HoTen": document.getElementById("HoTen")? document.getElementById("HoTen").value : "",
   "TrieuChung": document.getElementById("TrieuChung")? document.getElementById("TrieuChung").value : "",
   "LoaiBenh": document.getElementById("LoaiBenh")? document.getElementById("LoaiBenh").value : "",
   "id": a
  }), headers: {
   'Content-Type': 'application/json'
  }
 }).then(res => res.json()).then(data => {
        alert("Lưu thành công");
        location.reload();
 })
}




