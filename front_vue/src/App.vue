<script setup>
import VBtn from './components/VBtn.vue'
import { ref } from "vue"
import SMO from './SMO.vue';
const stateShow = ref("")
</script>

<template>
<div class="main-container">
  <div v-if="!stateShow">
    <VBtn value="Одноканальные СМО с ожиданием" @click="stateShow = '/api/solveSMO1Await'"/>
    <VBtn value="Одноканальные СМО с отказом" @click="stateShow = '/api/solveSMO1reject'" />
    <VBtn value="Многоканальные СМО с отказом" @click="stateShow = '/api/solveSMOMultiReject'"/>
  </div>
  <SMO v-if="stateShow" :url="stateShow" @back="stateShow = ''"/>
</div>
</template>

<style>
.main-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  max-width: 300px;
  margin: 0 auto;
}
</style>