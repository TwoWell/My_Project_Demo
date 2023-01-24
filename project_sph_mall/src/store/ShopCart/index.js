import { reqCartList, reqDeleteCartById, reqUpdateCheckedById } from "../../api"
const state = {
    shopCartInfo: []
}
const mutations = {
    getShopCartInfo(state, shopCartInfo) {
        state.shopCartInfo = shopCartInfo
    }
}
const actions = {
    async getShopCart({ commit }) {
        let result = await reqCartList()
        //console.log(result)
        if (result.code == 200) {
            // console.log(result)
            commit('getShopCartInfo', result.data)
        }
    },
    async deleteCartById({ commit }, skuId) {
        let result = await reqDeleteCartById(skuId)
        //console.log(result)
        if (result.code == 200) {
            return 'ok'
        } else {
            return Promise.reject(new Error('删除购物车失败！'))
        }
    },
    async updateCheckedById({ commit }, { skuId, isChecked }) {
        let result = await reqUpdateCheckedById(skuId, isChecked)
        //console.log(result)
        if (result.code == 200) {
            return 'ok'
        } else {
            return Promise.reject(new Error('购物车勾选状态异常！'))
        }
    },
    deleteAllCheckedCart({ dispatch, getters }) {
        // console.log(context)
        // console.log(dispatch, getters.cartInfo.cartInfoList)
        let PromiseAll = []
        getters.cartInfo.cartInfoList.forEach(cart => {
            // console.log(cart)
            let promise = cart.isChecked == 1 ? dispatch('deleteCartById', cart.skuId) : ''
            PromiseAll.push(promise)
        });
        //只要p1 || p2 || ... 都成功，则成功，只要有一个失败，就都失败
        return Promise.all(PromiseAll)
    },
    updateCartAllChecked({ dispatch, getters }, isChecked) {
        // console.log(dispatch, getters, isChecked)
        // console.log(getters.cartInfo.cartInfoList)
        let PromiseAll = []
        getters.cartInfo.cartInfoList.forEach(cart => {
            isChecked == cart.isChecked ? '' : PromiseAll.push(dispatch('updateCheckedById', { skuId: cart.skuId, isChecked: isChecked }))
        });
        return Promise.all(PromiseAll)
    }
}

const getters = {
    cartInfo(state) {
        return state.shopCartInfo[0] || {}
        // console.log(state.shopCartInfo[0])
    }
}

export default {
    // namespace: true,
    state,
    mutations,
    actions,
    getters
}