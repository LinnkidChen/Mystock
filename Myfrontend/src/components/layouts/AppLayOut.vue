<template>
  <div>
    <div class="common-layout">
      <el-container>
        <app-aside />
        <el-container class="header-and-main">
          <el-scrollbar>
            <AppHeader />
            <el-main>
              <RouterView />
            </el-main>
          </el-scrollbar>
        </el-container>
      </el-container>
    </div>
  </div>
</template>

<script setup>
import AppAside from './AppAside.vue'
</script>

<style lang="scss" scoped>
.header-and-main {
  flex-direction: column;
  height: 100vh;
}
.el-main {
  padding-right: none;
}
</style>
