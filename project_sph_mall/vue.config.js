const { defineConfig } = require('@vue/cli-service')
// const NodePolyfillPlugin = require('node-polyfill-webpack-plugin')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  productionSourceMap: false,

  //代理跨域：配置文件修改后需要重启服务
  devServer: {
    proxy: {
      '/api': {
        //目标服务器，即请求最终发到哪
        target: 'http://gmall-h5-api.atguigu.cn'
      },
    }
  }
  // configureWebpack: {
  //   resolve: {
  //     alias: {},
  //     fallback: {
  //       //其他的如果不启用可以用 keyname :false，例如：crypto:false, 
  //       "crypto": require.resolve("crypto-browserify"),
  //       "stream": require.resolve("stream-browserify"),
  //       fs: false,
  //       net: false
  //     },
  //   },
  //   plugins: [new NodePolyfillPlugin()]
  // }
})
