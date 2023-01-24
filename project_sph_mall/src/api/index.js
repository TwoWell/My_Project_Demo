//当前这个模块，进行API统一管理
import requests from "./requests";
import requests_mock from "./requests_mock"

//参考接口文档
//三级联动接口
///api/product/getBaseCategoryList

//axios发请求返回结果Promise对象
export const reqCategoryList = () => requests({ url: '/product/getBaseCategoryList', method: 'get' })
// export const reqCategoryList = ()=>requests.get('/product/getBaseCategoryList') 这个也行
export const reqSearchInfo = (params) => requests({ url: '/list', method: 'post', data: params })
export const reqGoodsInfo = (skuid) => requests({ url: `/item/${skuid}`, method: 'get' })
//api/cart/addToCart/{ skuId }/{ skuNum } 添加购物车接口
export const reqAddOrUpdateShopCart = (skuId, skuNum) => requests({ url: `/cart/addToCart/${skuId}/${skuNum}`, method: 'post' })
//api/cart/cartList获取购物车数据接口地址
export const reqCartList = () => requests({ url: '/cart/cartList', method: 'get' })
//删除购物车数据/api/cart/deleteCart/{skuId}
export const reqDeleteCartById = (skuId) => requests({ url: `/cart/deleteCart/${skuId}`, method: 'delete' })
//切换选中商品的状态/api/cart/checkCart/{skuID}/{isChecked}
export const reqUpdateCheckedById = (skuId, isChecked) => requests({ url: `/cart/checkCart/${skuId}/${isChecked}`, method: 'get' })
//获取验证码 /api/user/passport/sendCode/phone
export const reqGetCode = (phone) => requests({ url: `/user/passport/sendCode/${phone}`, method: 'get' })
//注册接口/api/user/passport/register
export const reqUserRegister = (data) => requests({ url: `/user/passport/register`, data, method: 'post' })
//登录接口/api/user/passport/login
export const reqUserLogin = (data) => requests({ url: `/user/passport/login`, data, method: 'post' })
//带着token向服务器要用户信息/api/user/passport/auth/getUserInfo
export const reqUserInfo = () => requests({ url: `/user/passport/auth/getUserInfo`, method: 'get' })
//退出登录/api/user/passport/logout
export const reqLogout = () => requests({ url: `/user/passport/logout`, method: 'get' })
//订单交易页面信息（收件人信息接口不用了，接口文档没有，视频才有）/api/order/auth/trade
export const reqOrderInfo = () => requests({ url: `/order/auth/trade`, method: 'get' })
//提交订单/api/order/auth/submitOrder?tradeNo={tradeNo}
export const reqSubmitOrder = (tradeNo, data) => requests({ url: `/order/auth/submitOrder?tradeNo=${tradeNo}`, data, method: 'post' })
//获取订单信息/api/payment/weixin/createNative/{orderId}
export const reqPayInfo = (orderId) => requests({ url: `/payment/weixin/createNative/${orderId}`, method: 'get' })
//获取订单列表/api/order/auth/{page}/{limit}
export const reqMyOrderList = (page, limit) => requests({ url: `/order/auth/${page}/${limit}`, method: 'get' })

//发送到mock
export const reqGetBannerList = () => requests_mock.get('/banner')
// console.log("hbj")
export const reqGetFloorList = () => requests_mock.get('/floors')