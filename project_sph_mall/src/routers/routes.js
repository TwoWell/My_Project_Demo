// import Home from "../pages/Home"
import Login from "../pages/Login"
import Register from "../pages/Register"
import Search from "../pages/Search"
import Detail from "../pages/Detail"
import AddCartSuccess from "../pages/AddCartSuccess"
import ShopCart from "../pages/ShopCart"
import Trade from "../pages/Trade"
import Pay from "../pages/Pay"
import PaySuccess from "../pages/PaySuccess"
import Center from "../pages/Center"
import groupOrder from "../pages/Center/groupOrder"
import myOrder from "../pages/Center/myOrder"

export default [
    {
        path: "*",
        redirect: "/Home"
    },
    {
        path: "/Home",
        //路由懒加载举例，工作的时候都是这样引入，相当于按需引入，不会一下子就全部加载
        component: ()=>import('../pages/Home'),
        meta: { show: true }
    },
    {
        name: "Login",
        path: "/Login",
        component: Login,
        meta: { show: true }
    },
    {
        path: "/Register",
        component: Register,
        meta: { show: false }
    },
    {
        name: "Search",
        path: "/Search/:keyword?",
        component: Search,
        meta: { show: true }
    },
    {
        name: "Detail",
        path: "/Detail/:skuId",
        component: Detail,
        meta: { show: true }
    },
    {
        name: "AddCartSuccess",
        path: "/AddCartSuccess",
        component: AddCartSuccess,
        meta: { show: true }
    },
    {
        name: "ShopCart",
        path: "/ShopCart",
        component: ShopCart,
        meta: { show: true }
    },
    {
        name: "Trade",
        path: "/Trade",
        component: Trade,
        meta: { show: true },
        //路由独享守卫
        beforeEnter: (to, from, next) => {
            if (from.path == '/ShopCart') {
                next()
            } else {
                next(false)
            }
        }
    },
    {
        name: "Pay",
        path: "/Pay",
        component: Pay,
        meta: { show: true },
        beforeEnter: (to, from, next) => {
            if (from.path == '/Trade') {
                next()
            } else {
                next(false)
            }
        }
    },
    {
        name: "PaySuccess",
        path: "/PaySuccess",
        component: PaySuccess,
        meta: { show: true }
    },
    {
        name: "Center",
        path: "/Center",
        component: Center,
        meta: { show: true },
        children: [
            {
                path: 'groupOrder',
                component: groupOrder
            },
            {
                path: 'myOrder',
                component: myOrder
            },
            {
                path: '/Center',
                redirect: '/Center/myOrder'
            }
        ]
    }
]