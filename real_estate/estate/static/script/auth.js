async function hashPassword(password) {
    const msgUint8 = new TextEncoder().encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

async function signup() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    const hashedPassword = await hashPassword(password);
    const user = { email: email, password: hashedPassword };

    localStorage.setItem(email, JSON.stringify(user));
    alert("Signup successful! Please log in.");
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const userData = localStorage.getItem(email);

    if (!userData) {
        alert("User not found. Please sign up.");
        return;
    }

    const user = JSON.parse(userData);
    const hashedPassword = await hashPassword(password);

    if (hashedPassword === user.password) {
        alert("Login successful!");
        sessionStorage.setItem("loggedInUser", email);
        window.location.href = "/myapp/dashboard/";  // Redirect to dashboard
    } else {
        alert("Incorrect password.");
    }
}

function logout() {
    sessionStorage.removeItem("loggedInUser");
    alert("Logged out successfully.");
    window.location.href = "/myapp/sign-in/";  // Redirect to login page
}
