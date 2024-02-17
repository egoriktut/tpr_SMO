<template>
    <div>
      <table class="table">
        <tbody>
          <div v-for="(row, rowIndex) in tableData" :key="rowIndex">
            <div v-if="rowIndex === 0" style="min-width: 300px;">Времени доступа уровней памяти</div>
            <div v-else-if="rowIndex === 1">Объем уровней памяти </div>
            <div v-else-if="rowIndex === 2">Активность файлов </div>
            <div v-else-if="rowIndex === 3">Объем файлов </div>
              <td v-for="(cell, colIndex) in row" :key="colIndex">
                <input type="text" v-model="tableData[rowIndex][colIndex]" />
              </td>
          </div>
        </tbody>
      </table>
    </div>
</template>
  
<script setup>
import { ref } from 'vue';

const props = defineProps({
  tableData: {
    type: Array,
    default: []
  },
});

const rowIndexOn = ref(0)

const tableData = ref(props.tableData);
</script>

<style scoped>
  .table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    margin-top: 20px;
  }
  
  .table input[type="text"] {
    width: 50px;
    padding: 5px;
    border: 1px solid #ddd;
  }
</style>
