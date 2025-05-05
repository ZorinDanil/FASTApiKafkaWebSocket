const API_URL = "http://localhost:8001/profile/api/v1";


export async function get_profile(user_id) {
    try {
        const response = await fetch(`${API_URL}/${user_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка загрузки профиля');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}


export async function get_all_profiles() {
    try {
        const response = await fetch(`${API_URL}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка загрузки профиля');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}



export async function update_profile(user_id, user_data) {
    console.log(user_data);

    try {
        const response = await fetch(`${API_URL}/${user_id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000",
            },
            body: JSON.stringify(user_data)
        });
        
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка загрузки профиля');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}

export async function upload_profile_picture(user_id, upload_profile_picture) {
    console.log(upload_profile_picture);

    try {
        const response = await fetch(`${API_URL}/${user_id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000",
            },
            body: JSON.stringify(upload_profile_picture)
        });
        
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Ошибка загрузки профиля');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error.message || error);
        throw error; // Перебрасываем ошибку для обработки в компоненте
    }
}
