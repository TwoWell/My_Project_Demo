import { reqSearchInfo } from "../../api"
const state = {
    SearchList: {}
}
const mutations = {
    getSearchList(state, SearchList) {
        //console.log(state, CateGoryList)
        state.SearchList = SearchList
    }
}
const actions = {
    async postSearchList({ commit }, params = {}) {
        let result = await reqSearchInfo(params)
        //console.log(result)
        if (result.code == 200) {
            commit('getSearchList', result.data)
        }
    }
}
const getters = {
    goodsList(state){
        return state.SearchList.goodsList || []
    },
    trademarkList(state){
        return state.SearchList.trademarkList || []
    },
    attrsList(state){
        return state.SearchList.attrsList || []
    }
}

export default {
    // namespace: true,
    state,
    mutations,
    actions,
    getters
}