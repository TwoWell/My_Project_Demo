import { reqOrderInfo } from "../../api"
const state = {
    orderInfo: {}
}
const mutations = {
    orderInfo(state, orderInfo) {
        //console.log(state, CateGoryList)
        state.orderInfo = orderInfo
    }
}
const actions = {
    async getOrderInfo({ commit }) {
        let result = await reqOrderInfo()
        //console.log(result)
        if (result.code == 200) {
            commit('orderInfo', result.data)
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