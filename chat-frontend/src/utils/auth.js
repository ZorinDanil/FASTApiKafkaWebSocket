export function setToken(token) {
    localStorage.setItem('token', token);
}

export function getToken() {
    return localStorage.getItem('token');
}

export function removeToken() {
    localStorage.removeItem('token');
}

export function setUserId(user_id){
    localStorage.setItem('user_id', user_id);
}

export function getUserId(){
    return localStorage.getItem('user_id');
}