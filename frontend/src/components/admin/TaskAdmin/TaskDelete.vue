<template>
  <div class="task-delete">
    <div class="card">
      <div class="card-body">
        <h3 class="card-title mb-4">
          <i class="bi bi-trash me-2"></i> Удалить задачу
        </h3>

        <div class="input-group mb-3">
          <input
            v-model.number="taskId"
            type="number"
            class="form-control"
            placeholder="Введите ID задачи"
          />
          <button
            class="btn btn-danger"
            @click="confirmDelete"
            :disabled="!taskId"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'
import axios from 'axios'

const $toast = useToast()
const taskId = ref(null)

const confirmDelete = async () => {
  if (!taskId.value) {
    $toast.error('Пожалуйста, введите корректный ID задачи.')
    return
  }

  try {
    const response = await axios.delete(`https://127.0.0.1:8000/tasks/${taskId.value}/`)
    
    if (response.status === 200) {
      $toast.success(`Задача с ID ${taskId.value} поставлена в очередь на удаление!`)
      taskId.value = null // Сбросить поле ввода
    }
  } catch (error) {
    console.error('Ошибка при удалении задачи:', error)
    
    if (error.response) {
      if (error.response.status === 404) {
        $toast.error(`Задача с ID ${taskId.value} не найдена.`)
      } else {
        $toast.error('Ошибка на сервере. Попробуйте позже.')
      }
    } else {
      $toast.error('Не удалось подключиться к серверу.')
    }
  }
}
</script>

<style scoped>
.task-delete {
  max-width: 500px;
  margin: 2rem auto;
}

.card {
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.5rem;
  color: #dc3545;
}

.input-group input {
  border-radius: 0.375rem;
  padding: 0.75rem;
  font-size: 1rem;
}

.btn-danger {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
