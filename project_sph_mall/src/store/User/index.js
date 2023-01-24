import { reqGetCode, reqUserRegister, reqUserLogin, reqUserInfo, reqLogout } from "../../api"
import { setLoginToken, getLoginToken, removeToken } from "../../utils/loginToken"
const state = {
    code: '',
    token: getLoginToken(),
    userInfo: {}
}
const mutations = {
    getCodeInfo(state, code) {
        state.code = code
    },
    getRegisterInfo(state, token) {
        state.token = token
    },
    getUserInfo(state, userInfo) {
        state.userInfo = userInfo
    },
    clearUserInfo(state) {
        state.userInfo = {}
        state.token = ''
        removeToken()
    }
}
const actions = {
    async getCode({ commit }, phone) {
        let result = await reqGetCode(phone)
        // console.log(result)
        if (result.code == 200) {
            commit('getCodeInfo', result.data)
            return 'ok'
        } else {
            return Promise.reject(new Error('获取验证码失败！'))
        }
    },
    async getUserRegisterInfo({ commit }, user) {
        let result = await reqUserRegister(user)
        // console.log(user)
        if (result.code == 200) {
            // commit('getRegisterInfo', result.data)
            return 'ok'
        } else {
            return Promise.reject(new Error('注册失败！'))
        }
    },
    async userLoginInfo({ commit }, data) {
        let result = await reqUserLogin(data)
        // console.log(user)
        if (result.code == 200) {
            commit('getRegisterInfo', result.data.token)
            setLoginToken(result.data.token)
            return 'ok'
        } else {
            return Promise.reject(new Error('登录失败！'))
        }
    },
    async getUserInfo({ commit }) {
        let result = await reqUserInfo()
        // console.log(result)
        if (result.code == 200) {
            commit('getUserInfo', result.data)
            return 'ok'
        } else {
            return Promise.reject(new Error('获取用户信息失败！'))
        }
    },
    async userLogout({ commit }) {
        let result = await reqLogout()
        // console.log(result)
        if (result.code == 200) {
            commit('clearUserInfo')
            return 'ok'
        } else {
            return Promise.reject(new Error('用户退出登录失败！'))
        }
    }
}
const getters = {}

export default {
    // namespace: true,
    state,
    mutations,
    actions,
    getters
}