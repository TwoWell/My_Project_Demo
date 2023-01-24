//对axios进行二次封装
import axios from "axios";
import nprogress from 'nprogress';//引入进度条，还需要引入样式
import 'nprogress/nprogress.css';
import store from "@/store";

//1：利用axios对象方法create，去创建一个axios实例
//2：request就是axios，只不过稍微配置一下
const requests = axios.create({
    //例如：请求的是/api/hbj/haha，则为/hbj/haha
    baseURL: "/api",
    timeout: 5000
})


//请求拦截器：在请求发出去之前，拦截器可以检测到，从而在请求发出去之前做一些事情
requests.interceptors.request.use((config) => {
    nprogress.start();
    //config：配置对象，对象里面有一个属性很重要，header请求头
    if (store.state.Detail.uuid_token) {
        config.headers.userTempId = store.state.Detail.uuid_token
    }
    if (store.state.User.token) {
        config.headers.token = store.state.User.token
    }
    return config;
})

//响应拦截器；可以在成功和失败的回调做一些事情
requests.interceptors.response.use((res) => {
    nprogress.done();
    //成功的回调函数：服务器响应数据回来以后，响应拦截器可以检测到，可以做一些事情
    return res.data;
}, (erro) => {
    //响应失败的回调
    return Promise.reject(new Error("faile !!"))
})



//对外暴露
export default requests;