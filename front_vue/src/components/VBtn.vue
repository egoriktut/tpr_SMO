<template>
    <button class="button-size" :disabled="props.disable">
      {{ props.value }}
    </button>
</template>
  
<script setup>
const props = defineProps({
  value: {
    type: String,
    default: '',
  },
  disable: {
    type: Boolean,
    default: false,
  }
});
</script>
  
<style scoped>
.button-size {
  padding: 10px 20px;
  margin: 10px;
  background-color: #3498db; 
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  outline: none;
  transition: background-color 0.2s ease-in-out;

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
}
  
.button-size:hover {
  background-color: #2c7eb5;
}
</style>
  