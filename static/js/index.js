// $(window).bind('beforeunload', function (e) {
//     console.log(e);
//     return '';

// });

if (window.performance) {
	console.info("window.performance works fine on this browser");
}
if (performance.navigation.type == 1) {
	console.info("This page is reloaded");
}
else {
	console.info("This page is not reloaded");
}

function login() {
	location.href = "https://account.kkbox.com/oauth2/authorize?response_type=code&client_id=8fee04af2d27c0c0e5125b86dfdf88f4&state=123&redirect_uri=https%3A%2F%2Fhackathon.ntouo.tw%2Fredirect"
	// location.href = "https://account.kkbox.com/oauth2/authorize?response_type=code&client_id=e831088656167120a490b9991a985f45&state=123&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect";
}
