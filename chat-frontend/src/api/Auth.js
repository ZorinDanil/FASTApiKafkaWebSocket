const API_URL = "/auth/api/v1";


export async function register(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка регистрации');
        }

        return response.json();
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}


export async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `username=${username}&password=${password}`
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка Входа');
        }

        return response.json();
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}