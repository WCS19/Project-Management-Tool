async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch('https://localhost:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
    } else {
        alert(data.message);
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('https://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.message);
            console.error('Login error:', errorData);
            return;
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('task-form').style.display = 'block';
        getTasks();
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
}

async function createTask() {
    const token = localStorage.getItem('token');
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;

    const response = await fetch('https://localhost:5000/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title, description })
    });

    if (response.ok) {
        getTasks();
    } else {
        alert('Error creating task');
    }
}

async function getTasks() {
    const token = localStorage.getItem('token');

    const response = await fetch('https://localhost:5000/tasks', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    if (response.ok) {
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        data.forEach(task => {
            const li = document.createElement('li');
            li.textContent = `${task.title} - ${task.description}`;
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = () => deleteTask(task.id);
            li.appendChild(deleteButton);
            taskList.appendChild(li);
        });
    } else {
        alert('Error fetching tasks');
    }
}

async function deleteTask(taskId) {
    const token = localStorage.getItem('token');

    const response = await fetch(`https://localhost:5000/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        getTasks();
    } else {
        alert('Error deleting task');
    }
}