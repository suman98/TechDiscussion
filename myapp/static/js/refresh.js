
function like(divid,type1){
	var el=document.getElementById(divid);
	// window.open("/like_view?question_id="+divid+"&like_view="+type1)
     $(el).load("/like_view?question_id="+divid+"&like_view="+type1);
	return false;
	

}

function profile_refresh(user_id,type1){
	// window.open("/profile?answer_q="+user_id+"&type1="+type1)
     $('#profile_refresh').load("/profile?answer_q="+user_id+"&type1="+type1);
	return false;
	
}
function comment(){
var form = document.getElementById('formcomment');
var formData = new FormData(form);
var xhr = new XMLHttpRequest();
// Add any event handlers here...
xhr.open('POST', '/post_ans/', true);
xhr.send(formData);
}
function message(){
var form = document.getElementById('Message');
var formData = new FormData(form);
var xhr = new XMLHttpRequest();
// Add any event handlers here...
xhr.open('POST', '/message/', true);
xhr.send(formData);
}


function report(question_id){
	var report_msg=prompt("Say what happed !!");
	if (report_msg=="" ||report_msg==null){
		return false;
	}
	else{
var xhr = new XMLHttpRequest();
// Add any event handlers here...
xhr.open('GET', "/report?report_msg="+report_msg+"&question_id="+question_id, true);
xhr.send();

		// $('#').load("/report?report_msg="+report_msg+"&question_id="+question_id);
		alert("Thank you will take action soon");
	}

}
function topics(topics){
	window.location.href="/?select="+topics
	return false;
}
function conform_delete(id1,t){

	var r = confirm("Are you sure you want to delete");
  if (r == true) {
  var xhr = new XMLHttpRequest();
// Add any event handlers here...
if (t=="q"){
xhr.open('GET', "/delete?question_id="+id1, true);
xhr.send();
}
if (t=="a"){
	xhr.open('GET', "/delete?answer_id="+id1, true);
xhr.send();
}
location.reload();
	return false;
	}
}
function Notification(){
	// window.open("/Notification?noti=ok");
	$("#Notification").load("/Notification?noti=ok");
	return false;

}
function Message(type){
// window.open("/message?show_msg="+type);

	$("#Notification").load("/message?show_msg="+type);
	return false;

}
function arrange_ans(question_id,type){
	// window.open("/ans_sort?question_id="+question_id);
	if (type=="like"){
	$("#ans_refresh").load("/ans_sort?question_id="+question_id);
	return false
}
else{
	// window.open("/ans_sort?ans_latest="+question_id);
	$("#ans_refresh").load("/ans_sort?ans_latest="+question_id);
	return false
}
}