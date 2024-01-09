<template>
  <el-aside>
    <el-scrollbar>
      <el-menu router :collapse="isCollapse">
        <a href="/" class="logo">
          <img src="@/assets/icon.png" alt="" />
          <h1>MyStock</h1>
        </a>
        <el-menu-item index="/">
          <el-icon><IEpSetting /></el-icon><span>我的指标</span>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><IEpSetting /></el-icon><span>我的自选股</span>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><IEpSetting /></el-icon><span>查看指标via股票</span>
        </el-menu-item>
        <el-menu-item class="menu-button">
          <el-button
            size="small"
            @click="
              () => {
                isCollapse = !isCollapse
              }
            "
            >折叠</el-button
          >
        </el-menu-item>
      </el-menu>
    </el-scrollbar>
  </el-aside>
</template>

<script setup lang="ts">
import { isCollapse } from './isCollapse'
</script>

<style lang="scss">
.el-aside {
  width: auto;
  height: 100vh;
  background-color: #66b1ff;
}
.el-menu {
  background-color: #a6a9ad;
  width: 200px;
  height: 100vh;
  justify-content: center;
  &.el-menu--collapse {
    width: 64px;
    & h1 {
      display: none;
    }
  }
}
.el-menu-item {
  display: flex;
  padding: 1px;
}
.menu-button {
  display: flex;
  justify-content: center;
  align-items: center;

  /* Your styles for the menu button */
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  background-color: #4e8e2f;
  font-size: 15px;
  height: 60px;
  img {
    width: 40px;
    height: 40xpx;
  }
}
</style>
