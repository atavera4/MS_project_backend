
console.log("vid js file");
function PlayVideo() {
	var d = new Date();
	var str ='pic.jpeg';
	document.getElementById("video_id").src = "pic.jpeg?ver" + d.getTime();

	return;
}
setInterval("PlayVideo()", 100);
