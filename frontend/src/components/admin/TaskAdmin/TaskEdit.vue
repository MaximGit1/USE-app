<template>
    <div class="task-section">
      <div class="card task-card">
        <div class="card-body">
          <h3 class="card-title mb-4">
            <i class="bi bi-pencil-square me-2"></i>Редактировать задачу
          </h3>
  
          <!-- Форма редактирования -->
          <form @submit.prevent="updateTask">
            <!-- Поля аналогичные TaskAdd.vue -->
            <button type="submit" class="btn btn-warning" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              Обновить задачу
            </button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useToast } from 'vue-toast-notification'
  import 'vue-toast-notification/dist/theme-sugar.css'
  
  const $toast = useToast()
  const loading = ref(false)
  const task = ref(null)
  
  const updateTask = async () => {
    // Логика обновления задачи
  }
  </script>
  
  <style scoped>
  .task-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: none;
  }
  
  .markdown-editor {
    min-height: 300px;
    resize: vertical;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 0.8rem;
  }
  
  .preview-wrapper {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 1rem;
    height: 100%;
    min-height: 318px;
    background: #f8f9fa;
  }
  
  .resizable {
    resize: vertical;
    min-height: 100px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #495057;
  }
  
  .form-control-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
  
  .btn-primary {
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 768px) {
    .markdown-editor {
      min-height: 200px;
    }
  
    .preview-wrapper {
      min-height: 200px;
      margin-top: 1rem;
    }
  }
  </style>