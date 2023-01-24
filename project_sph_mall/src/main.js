import Vue from 'vue'
import App from './App.vue'

import routers from "./routers"
import store from "./store"
import TypeNav from "./components/TypeNav"
import Carousel from "./components/Carousel"
import Pagination from "./components/Pagnation"

Vue.config.productionTip = false
Vue.component(TypeNav.name, TypeNav)
Vue.component(Carousel.name, Carousel)
Vue.component(Pagination.name, Pagination)

//测试请求接口
// import { reqCategoryList } from './api'
// reqCategoryList();
import "@/mock/mockServe"
import "swiper/css/swiper.css"
//全局引入API，并挂载到Vue的原型对象上，这样全局组件不用引入就能直接调用
import * as API from "./api"

//饿了么使用有两种方式进行注册，看官网
import { Button, MessageBox, Message } from 'element-ui'
Vue.component(Button.name, Button);
// Vue.component(MessageBox.name, MessageBox);
Vue.prototype.$msgbox = MessageBox
Vue.prototype.$alert = MessageBox.alert
Vue.prototype.$message = Message

import '@/plugins/validate'

new Vue({
  render: h => h(App),
  beforeCreate() {
    Vue.prototype.$bus = this
    Vue.prototype.$API = API
  },
  router: routers,
  store
}).$mount('#app')
