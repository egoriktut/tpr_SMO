<template>
  <input class="input-size" v-model="inputValue" :placeholder="props.holder" />
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  value: {
    type: String,
    default: '',
  },
  holder: {
    type: String,
    default: "",
  }
});

const inputValue = ref(props.value);

watch(() => props.value, (newValue) => {
  inputValue.value = newValue;
});
</script>

<style scoped>
.input-size {
  width: 200px;
  padding: 10px;
  margin: 10px;
  border: 2px solid #3498db;
  border-radius: 10px;
  background-color: #f0f0f0;
  color: #333;
  font-size: 16px;
  outline: none;
  transition: border 0.2s ease-in-out;
}

.input-size:focus {
  border-color: #e74c3c;
  box-shadow: 0 0 5px rgba(231, 76, 60, 0.5);
}
</style>
