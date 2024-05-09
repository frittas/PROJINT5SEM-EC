<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <div class="video">
    <video src="localhost:5000" autoplay type="video/mp4">
    </video>
  </div>
  <div class="side">
  </div>
</template>

<style scoped>
.video {
  border: 1px solid black;
  min-width: 50vh;
}

.side {
  border: 1px solid red;
  min-width: 50vh;
}
</style>
