

var btn = document.getElementById('login');

btn.addEventListener('click', () => {
    const re_con = new RegExp(".*@student.gsu.edu");
    const re_jud = new RegExp(".*@gsu.edu");
    var email = document.getElementById('email').value;
    console.log("email: ", email)
    if(re_jud.test(email)){
        self.window.location.href = "judge/posters";
    }
    else if(re_con.test(email)){
        self.window.location.href = "contestant/upload_poster";
    }
    else {
        console.log('[invalid email] must be a gsu associated email address');
        alert('[invalid email] must be a gsu associated email address');
    }
});
