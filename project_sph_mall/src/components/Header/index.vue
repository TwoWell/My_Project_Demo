<template>
    <header class="header">
        <!-- 头部的第一行 -->
        <div class="top">
            <div class="container">
                <div class="loginList">
                    <p>尚品汇欢迎您！</p>
                    <p v-if="!userName">
                        <span>请</span>
                        <router-link to="/Login">登录</router-link>
                        <router-link to="/Register" class="register">免费注册</router-link>
                    </p>
                    <p v-else>
                        <a>{{ userName }}</a>
                        <a class="register" @click="logOut">退出登录</a>
                    </p>
                </div>
                <div class="typeList">
                    <router-link to="/Center/myOrder">我的订单</router-link>
                    <router-link to="/ShopCart">我的购物车</router-link>
                    <a href="###">我的尚品汇</a>
                    <a href="###">尚品汇会员</a>
                    <a href="###">企业采购</a>
                    <a href="###">关注尚品汇</a>
                    <a href="###">合作招商</a>
                    <a href="###">商家后台</a>
                </div>
            </div>
        </div>
        <!--头部第二行 搜索区域-->
        <div class="bottom">
            <h1 class="logoArea">
                <router-link class="logo" to="/Home">
                    <img src="@/assets/images/logo.png" alt="">
                </router-link>
            </h1>
            <div class="searchArea">
                <form action="###" class="searchForm">
                    <input type="text" id="autocomplete" class="input-error input-xxlarge" v-model="keyword" />
                    <button class="sui-btn btn-xlarge btn-danger" type="button" @click="goSearch">搜索</button>
                </form>
            </div>
        </div>
    </header>
</template>

<script>
import router from '@/routers'
import { mapGetters } from 'vuex'

export default {
    name: "Header",
    data() {
        return {
            keyword: ""
        };
    },
    computed: {
        ...mapGetters(["trademarkList"]),
        userName() {
            return this.$store.state.User.userInfo.name;
        }
    },
    methods: {
        goSearch() {
            // console.log(this.trademarkList)
            if (this.$route.path != "/Home" && this.trademarkList.length) {
                if (this.trademarkList[0]["tmName"] == this.keyword && this.$route.path != "/Home") {
                    return;
                }
            }
            // console.log(this.trademarkList[0]['tmName'])
            //如果通过品牌图标筛选了，搜索框搜索同样的名字就不发请求了，避免面包屑上有多个同样的标签
            if (this.$route.query) {
                let location = { name: "Search", params: { keyword: this.keyword || undefined } };
                location.query = this.$route.query;
                this.$router.push(location, () => { });
            }
        },
        async logOut() {
            try {
                await this.$store.dispatch("userLogout");
                this.$router.push("/Home", () => { });
            }
            catch (error) {
                alert(error.message);
            }
        }
    },
    mounted() {
        this.$bus.$on("clearKeyword", () => {
            this.keyword = "";
        });
    },
    components: { router }
}
</script>

<style lang="less">
.header {

    // background-color: #eaeaea;
    &>.top {
        background-color: #eaeaea;
        height: 30px;
        line-height: 30px;

        .container {
            background-color: #eaeaea;
            width: 1200px;
            margin: 0 auto;
            overflow: hidden;

            .loginList {
                float: left;

                p {
                    float: left;
                    margin-right: 10px;

                    .register {
                        border-left: 1px solid #b3aeae;
                        padding: 0 5px;
                        margin-left: 5px;
                    }
                }
            }

            .typeList {
                float: right;

                a {
                    padding: 0 10px;

                    &+a {
                        border-left: 1px solid #b3aeae;
                    }
                }

            }

        }
    }

    &>.bottom {
        width: 1200px;
        margin: 0 auto;
        overflow: hidden;

        .logoArea {
            float: left;

            .logo {
                img {
                    width: 175px;
                    margin: 25px 45px;
                }
            }
        }

        .searchArea {
            float: right;
            margin-top: 35px;

            .searchForm {
                overflow: hidden;

                input {
                    box-sizing: border-box;
                    width: 490px;
                    height: 32px;
                    padding: 0px 4px;
                    border: 2px solid #ea4a36;
                    float: left;

                    &:focus {
                        outline: none;
                    }
                }

                button {
                    height: 32px;
                    width: 68px;
                    background-color: #ea4a36;
                    border: none;
                    color: #fff;
                    float: left;
                    cursor: pointer;

                    &:focus {
                        outline: none;
                    }
                }
            }
        }
    }
}
</style>