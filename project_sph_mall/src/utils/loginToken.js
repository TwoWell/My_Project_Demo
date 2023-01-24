export const setLoginToken = (token) => {
    localStorage.setItem('LoginToken', token)
}
export const getLoginToken = () => {
    return localStorage.getItem('LoginToken')
}
export const removeToken = () => {
    localStorage.removeItem('LoginToken')
}