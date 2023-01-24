import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
import store from "../store";

Vue.use(VueRouter)

let router = new VueRouter({
    //或者直接简写routes
    routes: routes,
    scrollBehavior(to, from, savedPosition) {
        // 始终滚动到顶部
        return { y: 0 }
    }
})

//路由全局守卫
router.beforeEach(async (to, from, next) => {
    // alert("全局路由守卫！")
    // console.log(to, from, next)
    // console.log(store)
    let token = store.state.User.token
    let name = store.state.User.userInfo.name
    if (token) {
        //登录后就不能URL直接去login了
        if (to.path == '/Login') {
            next('/Home')
            //登录后去其他页面，刷新的时候因为只有home派发获取用户信息的action，会导致在其他页面刷新之后用户信息就丢失了
        } else {
            if (name) {
                next()
            } else {
                try {
                    await store.dispatch("getUserInfo")
                    next()
                } catch (error) {
                    //token可能失效,清空失效的用户信息，然后放行至登录页面
                    // alert(error.message)
                    await store.dispatch("userLogout")
                    next('/Login')
                }
            }
        }
    } else {
        //未登录的情况:不能去交易相关，支付相关，个人中心(注意，路由独享守卫已经拦了)
        let toPath = to.path
        if (toPath.indexOf('/Center') != -1) {
            next('/Login?redirect=' + toPath)
        } else {
            next()
        }
    }
})

export default router