import { reqGoodsInfo, reqAddOrUpdateShopCart } from "../../api"
import { getUUID } from "@/utils/uuid_token"
const state = {
    GoodsInfo: {},
    //封装游客身份模块，生成一个游客身份id
    uuid_token: getUUID()
}
const mutations = {
    getGoodsInfo(state, GoodsInfo) {
        // console.log(GoodsInfo)
        state.GoodsInfo = GoodsInfo
    }
}
const actions = {
    async getGoodsList({ commit }, skuID) {
        let result = await reqGoodsInfo(skuID)
        //console.log(result)
        if (result.code == 200) {
            commit('getGoodsInfo', result.data)
        }
    },
    async addOrUpdateShopCart({ commit }, { skuID, skuNum }) {
        let result = await reqAddOrUpdateShopCart(skuID, skuNum)
        //console.log(result)
        if (result.code == 200) {
            return 'ok'
        } else {
            return Promise.reject(new Error('加入购物车失败！'))
        }
    }
}

const getters = {
    categoryView(state) {
        return state.GoodsInfo.categoryView || {}
    },
    skuInfo(state) {
        return state.GoodsInfo.skuInfo || {}
    },
    spuSaleAttrList(state) {
        return state.GoodsInfo.spuSaleAttrList || {}
    }
}

export default {
    namespace: true,
    state,
    mutations,
    actions,
    getters
}