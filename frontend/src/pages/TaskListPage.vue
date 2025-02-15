<script setup>
import { ref, onMounted } from 'vue'
import TaskCard from '../components/TaskCard.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const tasks = ref([])

// Функция загрузки задач с API
const fetchTasks = async () => {
    try {
        const response = await fetch('https://127.0.0.1:8000/tasks/base/?offset=0&limit=10')
        const data = await response.json()
        
        // Приводим данные API к формату, который используется в TaskCard
        tasks.value = data.map(task => ({
            id: task.id,
            type: task.type,
            body: task.body,
            timeLimit: task.time_limit  // Приводим к camelCase
        }))
    } catch (error) {
        console.error("Ошибка загрузки задач:", error)
    }
}

// Загружаем задачи при монтировании компонента
onMounted(fetchTasks)

const goToDetail = (task) => {
    router.push({
        path: `/${task.id}/detail`,
        state: task // Передаем объект с данными
    })
}
</script>

<template>
    <div class="container">
        <h1>Список задач</h1>
        <TaskCard 
            v-for="task in tasks" 
            :key="task.id"
            :id="task.id"
            :type="task.type"
            :body="task.body"
            :timeLimit="task.timeLimit"
            @click="goToDetail(task)"
        />
    </div>
</template>
