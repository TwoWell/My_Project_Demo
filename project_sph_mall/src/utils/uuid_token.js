import { v4 as uuidv4 } from 'uuid'

//通过UUID工具生成随机游客临时身份
export const getUUID = () => {
    let uuid_token = localStorage.getItem('UUIDTOKEN')
    if (!uuid_token) {
        uuid_token = uuidv4()
        localStorage.setItem('UUIDTOKEN', uuid_token)
    }
    return uuid_token
}