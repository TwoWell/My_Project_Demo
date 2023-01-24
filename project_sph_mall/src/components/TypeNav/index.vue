<template>
  <div class="type-nav">
    <div class="container" @mouseleave="LeaveShow">
      <h2 class="all" @mouseover="EnterShow">全部商品分类</h2>
      <nav class="nav">
        <a href="###">服装城</a>
        <a href="###">美妆馆</a>
        <a href="###">尚品汇超市</a>
        <a href="###">全球购</a>
        <a href="###">闪购</a>
        <a href="###">团购</a>
        <a href="###">有趣</a>
        <a href="###">秒杀</a>
        <!-- <a href="###">{{ Home }}</a> -->
      </nav>
      <Transition name="sort">
        <div class="sort" v-show="show">
          <div class="all-sort-list2" @click="toSearch">
            <div class="item" v-for="(c1, _) in CateGoryList" :key="c1.categoryId">
              <h3>
                <a :data-categoryName="c1.categoryName" :data-category1Id="c1.categoryId">{{ c1.categoryName }}</a>
                <!-- <router-link to="/search">{{ c1.categoryName }}</router-link> -->
              </h3>
              <div class="item-list clearfix">
                <div class="subitem" v-for="(c2, _) in c1.categoryChild" :key="c2.categoryId">
                  <dl class="fore">
                    <dt>
                      <a :data-categoryName="c2.categoryName" :data-category2Id="c2.categoryId">{{
                        c2.categoryName
                      }}</a>
                    </dt>
                    <dd>
                      <em v-for="(c3, _) in c2.categoryChild" :key="c3.categoryId">
                        <a :data-categoryName="c3.categoryName" :data-category3Id="c3.categoryId">{{
                          c3.categoryName
                        }}</a>
                      </em>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "TypeNav",
  data() {
    return { show: true }
  },
  mounted() {
    if (this.$route.path != "/Home") {
      this.show = false
    }
  },
  computed: {
    // ...mapState(['Home', 'Search'])
    ...mapState("Home", { CateGoryList: "CateGoryList" })
  },
  methods: {
    toSearch(event) {
      let element = event.target
      let { categoryname, category1id, category2id, category3id } = element.dataset
      // let data_set = element.dataset
      // console.log(category1id)
      // console.log(category2id)
      if (categoryname) {
        let location = { name: "Search" }
        let query = { categoryName: categoryname }
        if (category1id) {
          query.category1Id = category1id
        } else if (category2id) {
          query.category2Id = category2id
        } else {
          query.category3Id = category3id
        }
        if (this.$route.params) {
          location.params = this.$route.params
          location.query = query
        }
        this.$router.push(location).catch(erro => { erro })
      }
    },
    EnterShow() {
      if (this.$route.path != "/Home") {
        this.show = true
      }
    },
    LeaveShow() {
      if (this.$route.path != "/Home") {
        this.show = false
      }
    }
  }
}
</script>

<style scoped lang="less">
.type-nav {
  border-bottom: 2px solid #e1251b;

  .container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    position: relative;

    .all {
      width: 210px;
      height: 45px;
      background-color: #e1251b;
      line-height: 45px;
      text-align: center;
      color: #fff;
      font-size: 14px;
      font-weight: bold;
    }

    .nav {
      a {
        height: 45px;
        margin: 0 22px;
        line-height: 45px;
        font-size: 16px;
        color: #333;
      }
    }

    .sort {
      position: absolute;
      left: 0;
      top: 45px;
      width: 210px;
      height: 461px;
      position: absolute;
      background: #fafafa;
      z-index: 999;

      .all-sort-list2 {
        height: 480px;
        overflow: hidden;

        .item {
          h3 {
            line-height: 30px;
            font-size: 14px;
            font-weight: 400;
            overflow: hidden;
            padding: 0 20px;
            margin: 0;

            a {
              color: #333;
            }
          }

          .item-list {
            display: none;
            position: absolute;
            width: 734px;
            min-height: 460px;
            background: #f7f7f7;
            left: 210px;
            border: 1px solid #ddd;
            top: 0;
            z-index: 9999 !important;

            .subitem {
              float: left;
              width: 650px;
              padding: 0 4px 0 8px;

              dl {
                border-top: 1px solid #eee;
                padding: 6px 0;
                overflow: hidden;
                zoom: 1;

                &.fore {
                  border-top: 0;
                }

                dt {
                  float: left;
                  width: 54px;
                  line-height: 22px;
                  text-align: right;
                  padding: 3px 6px 0 0;
                  font-weight: 700;
                }

                dd {
                  float: left;
                  width: 415px;
                  padding: 3px 0 0;
                  overflow: hidden;

                  em {
                    float: left;
                    height: 14px;
                    line-height: 14px;
                    padding: 0 8px;
                    margin-top: 5px;
                    border-left: 1px solid #ccc;
                  }
                }
              }
            }
          }

          &:hover {
            .item-list {
              display: block;
            }

            h3 {
              background-color: rgb(162, 203, 241);

              a {
                text-decoration: underline;
                cursor: pointer;
                color: purple;
              }
            }

            dt {
              a {
                text-decoration: underline;
                cursor: pointer;
                // color: purple;
              }
            }

            em {
              a {
                text-decoration: underline;
                cursor: pointer;
                // color: purple;
              }
            }
          }
        }
      }
    }

    .sort-enter {
      height: 0px;
    }

    .sort-enter-to {
      overflow: hidden;
      height: 461px;
    }

    .sort-enter-active {
      transition: all 0.6s linear;
    }
  }
}
</style>
