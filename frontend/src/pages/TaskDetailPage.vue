<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import TaskDetail from '../components/TaskDetail.vue'
import TaskEditor from '../components/TaskEditor.vue'

const route = useRoute()
const router = useRouter()
const task = ref(null)
const showInfo = ref(false)

const toggleInfo = () => {
    showInfo.value = !showInfo.value
}

async function checkPermission() {
    try {
        const response = await fetch('https://127.0.0.1:8000/auth/verify-role/?role=admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Добавьте заголовок авторизации если нужно:
                // 'Authorization': `Bearer ${your_token}`
            },
            credentials: 'include' // Если используете куки
        })
        
        if (!response.ok) throw new Error('Ошибка проверки прав')
        const data = await response.json()
        
        return data
    } catch (error) {
        console.error('Ошибка:', error)
        return false
    }
}

onMounted(async () => {
    try {
        // Проверка прав доступа
        const hasAccess = await checkPermission()
        if (!hasAccess) {
            router.push('/403')
            return
        }

        // Загрузка данных задачи
        const taskId = route.params.taskId

        if (history.state?.id) {
            task.value = history.state
        } else {
            const response = await fetch(`https://127.0.0.1:8000/tasks/base/${taskId}`)
            if (!response.ok) throw new Error("Ошибка загрузки данных")
            const data = await response.json()
            
            task.value = {
                id: data.id,
                type: data.type,
                body: data.body,
                timeLimit: data.time_limit
            }
        }
    } catch (error) {
        console.error("Ошибка:", error)
        router.push('/403')
    }
})
</script>

<template>
    <div class="container">
        <div v-if="task">
            <TaskDetail 
                :id="task.id"
                :type="task.type"
                :body="task.body"
                :timeLimit="task.timeLimit"
            />
            
            <TaskEditor 
                :showInfo="showInfo" 
                :toggleInfo="toggleInfo"
                :taskId="task.id"
            />
        </div>
        <p v-else>Загрузка...</p>
    </div>
    <div class="space"></div>
</template>

<style scoped>
.space {
    height: 200px;
}
</style>
