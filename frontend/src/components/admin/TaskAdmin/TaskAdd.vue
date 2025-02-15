<template>
    <div class="task-section">
      <div class="card task-card">
        <div class="card-body">
          <h3 class="card-title mb-4">
            <i class="bi bi-plus-circle me-2"></i>Добавить задачу
          </h3>
  
          <!-- Форма добавления -->
          <form @submit.prevent="createTask">
            <div class="row g-4">
              <!-- Левая колонка: Описание -->
              <div class="col-md-6">
                <div class="form-group">
                  <label class="form-label">Описание задачи (Markdown):</label>
                  <textarea
                    v-model="newTask.body"
                    class="form-control markdown-editor"
                    placeholder="Введите текст задачи..."
                    rows="10"
                    required
                  ></textarea>
                </div>
              </div>
  
              <!-- Правая колонка: Предпросмотр -->
              <div class="col-md-6">
                <div class="preview-wrapper">
                  <label class="form-label">Предпросмотр:</label>
                  <MarkdownRenderer :content="newTask.body" />
                </div>
              </div>
            </div>
  
            <!-- Нижний блок: Ответ и параметры -->
            <div class="row mt-4">
              <div class="col-md-8">
                <div class="form-group">
                  <label class="form-label">Ответ:</label>
                  <textarea
                    v-model="newTask.answer"
                    class="form-control resizable"
                    rows="3"
                    placeholder="Введите правильный ответ..."
                    required
                  ></textarea>
                </div>
              </div>
  
              <div class="col-md-4">
                <div class="row g-2">
                  <div class="col-6">
                    <div class="form-group">
                      <label class="form-label">Тип задачи:</label>
                      <select
                        v-model="newTask.type"
                        class="form-control form-control-sm"
                        required
                      >
                        <option value="4">Знание 4</option>
                        <option value="5">Знание 5</option>
                      </select>
                    </div>
                  </div>
  
                  <div class="col-6">
                    <div class="form-group">
                      <label class="form-label">Лимит (сек):</label>
                      <input
                        v-model.number="newTask.time_limit"
                        type="number"
                        class="form-control form-control-sm"
                        min="1"
                        required
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Кнопка отправки -->
            <div class="mt-4">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm"></span>
                Создать задачу
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useToast } from 'vue-toast-notification'
  import 'vue-toast-notification/dist/theme-sugar.css'
  import MarkdownRenderer from '../../MarkdownRenderer.vue'
  
  const $toast = useToast()
  const loading = ref(false)
  
  const newTask = ref({
    type: '4',
    body: '',
    answer: '',
    time_limit: 60
  })
  
  const createTask = async () => {
    try {
      loading.value = true
      const response = await fetch('https://127.0.0.1:8000/tasks/create/base/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask.value)
      })
  
      if (!response.ok) throw new Error('Ошибка создания задачи')
      const data = await response.json()
  
      $toast.success('Задача успешно создана!', {
        position: 'top-right',
        duration: 3000,
        dismissible: true
      })
  
      newTask.value = { type: '4', body: '', answer: '', time_limit: 60 }
    } catch (error) {
      $toast.error(error.message, {
        position: 'top-right',
        duration: 5000,
        dismissible: true
      })
    } finally {
      loading.value = false
    }
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