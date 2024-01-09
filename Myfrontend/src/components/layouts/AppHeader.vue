<template>
  <div>
    <el-header>
      <el-icon
        @click="
          () => {
            isCollapse = !isCollapse
          }
        "
      >
        <IEpExpand v-show="isCollapse" />
        <IEpFold v-show="!isCollapse" />
      </el-icon>

      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
        <el-breadcrumb-item>promotion management</el-breadcrumb-item>
        <el-breadcrumb-item>promotion list</el-breadcrumb-item>
        <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
  </div>
</template>

<script setup lang="ts">
import { isCollapse } from './isCollapse'

console.log(isCollapse)
</script>

<style lang="scss" scoped>
.el-header {
  display: flex;
  align-items: center;
  background-color: #3375b9;
  padding: 0 20px;
  height: 60px;
  .el-icon {
    margin-right: 20px;
    cursor: pointer;
  }
}
</style>
