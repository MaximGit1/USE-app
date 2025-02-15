<template>
    <div class="container my-5">
      <h1 class="mb-4">Теория программирования на Python</h1>
      
      <!-- Задание 4 -->
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title mb-3">Задание 4 - Основы Python</h2>
          <MarkdownRenderer :content="assignments[0].content.replace(/^ {2}/gm, '')" />
        </div>
      </div>
  
      <!-- Задание 5 -->
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title mb-3">Задание 5 - Работа с функциями</h2>
          <MarkdownRenderer :content="assignments[1].content.replace(/^ {2}/gm, '')" />
        </div>
      </div>
    </div>
</template>

<script setup>
  import { ref } from 'vue';
  import MarkdownRenderer from '../components/MarkdownRenderer.vue';
  
  const assignments = ref([
    {
      id: 4,
      content: `
  ### Основные концепции Python
  
  Python - интерпретируемый язык с динамической типизацией. Основные структуры данных:
  
  1. Списки
  2. Словари
  3. Кортежи
  
  **Пример создания списка:**
  \`\`\`python
  fruits = ['apple', 'banana', 'orange']
  print(fruits[0])  # Доступ по индексу
  \`\`\`
  
  **Работа с условиями:**
  \`\`\`python
  age = 18
  if age >= 18:
      print("Доступ разрешен")
  else:
      print("Доступ запрещен")
  \`\`\`
  `
    },
    {
      id: 5,
      content: `
  ### Функции в Python
  
  Функции создаются с помощью ключевого слова **def**
  
  **Простая функция:**
  \`\`\`python
  def greet(name):
      return f"Привет, {name}!"
      
  print(greet("Анна"))
  \`\`\`
  
  **Функция с аргументами по умолчанию:**
  \`\`\`python
  def power(base, exponent=2):
      return base ** exponent
      
  print(power(3))     # 9
  print(power(3, 3))  # 27
  \`\`\`
  `
    }
  ]);
  </script>
  
<style scoped>
  .card {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .card-title {
    color: #2c3e50;
    border-bottom: 2px solid #42b983;
    padding-bottom: 0.5rem;
  }
  </style>