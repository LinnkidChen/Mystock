<script setup>
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
import MainView from './views/MainView.vue'
import MainNavi from './components/MainNavi.vue'
</script>

<!-- <template>
  <header>
    <div class="wrapper">
      
      <MainView />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template> -->
<template>
<RouterView/>
</template>

<style>
</style>
