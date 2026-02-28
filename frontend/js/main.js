const API_BASE = '/api';

// Auth State
function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function isLoggedIn() {
    return !!getUser();
}

// Navigation Update
document.addEventListener('DOMContentLoaded', () => {
    updateNav();
});

function updateNav() {
    const navLinks = document.getElementById('nav-links');
    if (!navLinks) return;

    const user = getUser();
    if (user) {
        let dashboardLink = '';
        if (user.role === 'organizer') {
            dashboardLink = '<li><a href="/dashboard-organizer.html" class="hover:text-primary transition font-semibold">Organize</a></li>';
        } else {
            dashboardLink = '<li><a href="/dashboard-volunteer.html" class="hover:text-primary transition font-semibold">Dashboard</a></li>';
        }

        navLinks.innerHTML = `
            <li><a href="/index.html" class="hover:text-primary transition font-semibold">Home</a></li>
            <li><a href="/browse.html" class="hover:text-primary transition font-semibold">Events</a></li>
            <li><a href="/about.html" class="hover:text-primary transition font-semibold">Mission</a></li>
            ${dashboardLink}
            <li><button id="logout-btn" class="text-red-500 hover:text-red-700 font-bold transition">Logout</button></li>
        `;

        document.getElementById('logout-btn').addEventListener('click', logout);
    } else {
        navLinks.innerHTML = `
            <li><a href="/index.html" class="hover:text-primary transition font-semibold">Home</a></li>
            <li><a href="/browse.html" class="hover:text-primary transition font-semibold">Explore</a></li>
            <li><a href="/about.html" class="hover:text-primary transition font-semibold">Mission</a></li>
            <li><a href="/login.html" class="bg-primary text-white px-5 py-2 rounded-full hover:bg-red-800 transition font-semibold shadow-md">Join Now</a></li>
        `;
    }
}

// API Helpers
async function apiCall(endpoint, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    const options = {
        method,
        headers
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        return { ok: response.ok, data, status: response.status };
    } catch (error) {
        console.error('API Error:', error);
        return { ok: false, error };
    }
}

async function login(email, password) {
    console.log('DEBUG: Attempting login for', email);
    const res = await apiCall('/auth/login', 'POST', { email, password });
    console.log('DEBUG: Login response', res);
    if (res.ok) {
        console.log('DEBUG: Login successful, saving user and redirecting');
        localStorage.setItem('user', JSON.stringify(res.data.user));
        const redirectUrl = res.data.user.role === 'organizer' ? '/dashboard-organizer.html' : '/dashboard-volunteer.html';
        console.log('DEBUG: Redirecting to', redirectUrl);
        window.location.href = redirectUrl;
    } else {
        console.error('DEBUG: Login failed', res.data.error);
        alert(res.data.error || 'Login failed');
    }
}

async function register(name, email, password, role) {
    const res = await apiCall('/auth/register', 'POST', { name, email, password, role });
    if (res.ok) {
        console.log('DEBUG: Registration successful, logging in...');
        await login(email, password);
    } else {
        alert(res.data.error || 'Registration failed');
    }
}

async function logout(e) {
    e.preventDefault();
    await apiCall('/auth/logout', 'POST');
    localStorage.removeItem('user');
    window.location.href = '/index.html';
}
