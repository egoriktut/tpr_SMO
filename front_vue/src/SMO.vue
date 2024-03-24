<script setup>
import axios from 'axios'
import { computed, ref, defineEmits } from 'vue'
import VInput from './components/VInput.vue'
import VBtn from './components/VBtn.vue'

const props = defineProps({
  url: {
    type: String,
    default: ""
  }
})
const emit = defineEmits(["back"])
const t = ref("")
const l = ref("")
const m = ref("")
const n = ref("")
const inf = ref(false)
const info = ref("")
const imgInfo = ref("")

  
const canFetch = computed(() => {
  if (props.url === "/api/solveSMOMultiAwait") {
    return (
      t.value.replace(" ", "").length && l.value.replace(" ", "").length && m.value.replace(" ", "").length && n.value.replace(" ", "").length
      ) || t.value.replace(" ", "").length && l.value.replace(" ", "").length && n.value.replace(" ", "").length && inf.value
  };
  return t.value.replace(" ", "").length && l.value.replace(" ", "").length && m.value.replace(" ", "").length
})
  
const fetchData = () => {
  const data = ref("")
  if (props.url === "/api/solveSMOMultiAwait") {
    data.value = {
      t: t.value,
      l: l.value,
      m: m.value,
      n: n.value,
      inf: inf.value,
    };
  } else {
    data.value = {
      t: t.value,
      l: l.value,
      m: m.value,
    };
  };
  axios.post(
    props.url, 
    { data: data.value },
  ).then((response) => {
    info.value = response.data.msg
    if (props.url.includes("SMOMulti")) {
      imgInfo.value = response.data.img
    }
    info.value = response.data.msg
  })
}
</script>

<template>
  <div class="main-container">
    <div class="container">
      <VInput v-model="t" holder="Среднее время обработки"></VInput>
      <VInput v-model="l" holder="Интенсивность"></VInput>
      <VInput v-if="props.url === '/api/solveSMOMultiAwait'" v-model="n" holder="Количество каналов" />
      <VInput 
        v-if="
          props.url === '/api/solveSMO1Await' || props.url === '/api/solveSMOMultiAwait'
        "
        v-model="m" 
        holder="Размер очереди" 
      />
      <VInput v-else-if="props.url === '/api/solveSMO1reject'" v-model="m" holder="Время симуляции (мин)" />
      <VInput v-else-if="props.url === '/api/solveSMOMultiReject'" v-model="m" holder="Количество каналов" />
      <div v-if="props.url === '/api/solveSMOMultiAwait'" class="checkbox-container" @click="inf = !inf" >
        <input v-model="inf" type="checkbox"/>
        <p>Бесконечная очередь</p>
      </div>
      <VBtn value="Проверить" @click="fetchData" :disable="!canFetch"></VBtn>
      <VBtn value="Назад" @click="emit('back')"></VBtn>
    </div>
    
    <div v-if="info" style="min-width: 650px;">
      <div class="preview-message">
        <div v-for="i in info">
          {{ i }}
        </div>
      </div>
    </div>
    <img v-if="imgInfo" :src="imgInfo" style="display: flex; justify-content: center; object-fit: none; object-position: 0px -180px;">
  </div>
</template>

<style scoped>
.checkbox-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.checkbox-container:hover {
  cursor: pointer;
}


.main-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  max-width: 300px;
  margin: 0 auto;
}
.container{
  display: flex;
  flex-direction: column;
  max-width: 224px;
}
  
.preview-message {
  background-color: #E6F7FF;
  padding: 10px;
  border: 1px solid #91D5FF;
  border-radius: 5px;
}
</style>