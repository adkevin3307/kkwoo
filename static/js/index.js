$(window).bind('beforeunload', function (e) {
    console.log(e);
    return '';

});

function login()
{
	location.href = "https://account.kkbox.com/oauth2/authorize?response_type=code&client_id=8fee04af2d27c0c0e5125b86dfdf88f4&state=123&redirect_uri=https%3A%2F%2Fhackathon.ntouo.tw/redirect";
}