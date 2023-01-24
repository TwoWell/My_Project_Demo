<template>
  <div>
    <TypeNav />
    <ListContainer />
    <Recommend />
    <Rank />
    <Like />
    <Floor v-for="(floor, _) in FloorList" :key="floor.id" :list="floor" />
    <Brand />
  </div>
</template>

<script>

import ListContainer from "../Home/ListContainer"
import Recommend from "../Home/Recommend"
import Rank from "../Home/Rank"
import Like from "../Home/Like"
import Floor from "../Home/Floor"
import Brand from "../Home/Brand"

import { mapState } from "vuex"

export default {
  name: 'Home',
  components: {
    ListContainer,
    Recommend,
    Rank,
    Like,
    Floor,
    Brand
  },
  computed: {
    ...mapState("Home", { FloorList: "FloorList" })
  },
  mounted() {
    this.$store.dispatch("Home/getFloorList")
  }
}
</script>

<style scoped>

</style>
