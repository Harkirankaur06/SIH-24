// script.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    const forgotPassword = document.getElementById('forgot-password');
    const login = document.getElementById('login');
    const register = document.getElementById('register');

    showRegister.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    });

    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });

    forgotPassword.addEventListener('click', (e) => {
        e.preventDefault();
        alert('Forgot Password functionality is not implemented.');
    });

    login.addEventListener('submit', (e) => {
        e.preventDefault();
        // You can add additional validation here if needed
        // For now, just redirect to Current Info page
        window.location.href = 'current-info.html';
    });

    register.addEventListener('submit', (e) => {
        e.preventDefault();
        // You can add additional validation here if needed
        // For now, just redirect to Current Info page
        window.location.href = 'current-info.html';
    });
});
