async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('https://127.0.0.1:5001/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('task-container').style.display = 'block';
        getTasks();
    } catch (error) {
        console.error('Error during login:', error);
        alert('Error during login. Please try again.');
    }
}

async function getTasks() {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch('https://127.0.0.1:5001/tasks', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }

        const tasks = await response.json();
        const taskList = document.getElementById('task-list');
        const deleteTaskList = document.getElementById('delete-task-list');
        taskList.innerHTML = '';
        deleteTaskList.innerHTML = '';

        tasks.forEach(task => {
            const taskCard = document.createElement('div');
            taskCard.className = 'task-card';
            taskCard.innerHTML = `
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <input type="checkbox" onclick="toggleDeleteButton(this)">
                <button class="delete-button" onclick="deleteTask(${task.id})" style="display: none;">Delete</button>
            `;
            taskList.appendChild(taskCard);

            const deleteTaskItem = document.createElement('li');
            deleteTaskItem.innerHTML = `
                <input type="checkbox" class="delete-checkbox" data-task-id="${task.id}">
                ${task.title}
            `;
            deleteTaskList.appendChild(deleteTaskItem);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
        alert('Error fetching tasks. Please try again.');
    }
}

async function createTask() {
    const token = localStorage.getItem('token');
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;

    try {
        const response = await fetch('https://127.0.0.1:5001/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, description })
        });

        if (!response.ok) {
            throw new Error('Error creating task');
        }

        getTasks();
    } catch (error) {
        console.error('Error creating task:', error);
        alert('Error creating task. Please try again.');
    }
}

async function deleteTask(taskId) {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`https://127.0.0.1:5001/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error deleting task');
        }

        getTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Error deleting task. Please try again.');
    }
}

async function deleteSelectedTasks() {
    const checkboxes = document.querySelectorAll('.delete-checkbox:checked');
    const token = localStorage.getItem('token');

    try {
        for (const checkbox of checkboxes) {
            const taskId = checkbox.getAttribute('data-task-id');
            const response = await fetch(`https://127.0.0.1:5001/tasks/${taskId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Error deleting task');
            }
        }

        getTasks();
    } catch (error) {
        console.error('Error deleting tasks:', error);
        alert('Error deleting tasks. Please try again.');
    }
}

function toggleDeleteButton(checkbox) {
    const deleteButton = checkbox.nextElementSibling;
    if (checkbox.checked) {
        deleteButton.style.display = 'inline';
    } else {
        deleteButton.style.display = 'none';
    }
}

function toggleDeleteTaskList() {
    const deleteTaskList = document.getElementById('delete-task-list');
    if (deleteTaskList.style.display === 'none' || deleteTaskList.style.display === '') {
        deleteTaskList.style.display = 'block';
    } else {
        deleteTaskList.style.display = 'none';
    }
}

document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    login();
});

document.getElementById('task-container').addEventListener('submit', (e) => {
    e.preventDefault();
    createTask();
});
