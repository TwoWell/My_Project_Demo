import { reqCategoryList, reqGetBannerList, reqGetFloorList } from "../../api"

const state = {
    CateGoryList: [],
    BannerList: [],
    FloorList: [],
}
const mutations = {
    CateGoryList(state, CateGoryList) {
        //console.log(state, CateGoryList)
        state.CateGoryList = CateGoryList
    },
    BannerList(state, BannerList) {
        state.BannerList = BannerList
    },
    FloorList(state, FloorList) {
        state.FloorList = FloorList
    }
}
const actions = {
    async categoryList(context) {
        let result = await reqCategoryList()
        //console.log(result)
        if (result.code == 200) {
            context.commit('CateGoryList', result.data)
        }
    },
    async getBannerList({ commit }) {
        let result = await reqGetBannerList()
        // console.log(result)
        // console.log(context)
        if (result.code == 200) {
            commit('BannerList', result.data)
        }
    },
    async getFloorList({ commit }) {
        let result = await reqGetFloorList()
        if (result.code == 200) {
            commit('FloorList', result.data)
        }
    }
}
const getters = {}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}