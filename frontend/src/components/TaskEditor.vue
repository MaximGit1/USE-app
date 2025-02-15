<script setup>
import { ref, onMounted } from 'vue'
import CodeMirror from 'codemirror'

// Импорт стилей и модулей
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/yonce.css'
import 'codemirror/mode/python/python.js'
import 'codemirror/addon/edit/closebrackets.js'
import 'codemirror/addon/display/placeholder.js'
import 'codemirror/addon/scroll/scrollpastend.js'

const props = defineProps({
    showInfo: Boolean,
    toggleInfo: Function,
    taskId: Number
})

const editor = ref(null)
const codeEditor = ref(null)
const errorMessage = ref('')
const isButtonDisabled = ref(false)
const testResult = ref(null)

onMounted(() => {
    if (!editor.value) return

    codeEditor.value = CodeMirror.fromTextArea(editor.value, {
        mode: 'python',
        lineNumbers: true,
        theme: 'yonce',
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        smartIndent: true,
        autoCloseBrackets: true,
        placeholder: "Пишите код здесь...",
        scrollbarStyle: 'null'
    })
})

const send_task_to_run = async () => {
    if (!props.taskId) {
        errorMessage.value = 'Ошибка: задача не выбрана'
        return
    }
    
    const code = codeEditor.value.getValue()
    
    if (code.trim().length < 10) {
        errorMessage.value = 'Ошибка: код должен содержать не менее 10 символов.'
        testResult.value = null
        return
    }

    isButtonDisabled.value = true
    errorMessage.value = ''
    testResult.value = null

    try {
        const response = await fetch(`https://127.0.0.1:8000/tasks/run/${props.taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                task_id: props.taskId
            }),
            credentials: 'include'
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log('Received response:', data) // Добавлено логирование
        testResult.value = {
            res: data.res,
            completed_time: data.completed_time
        }
        
    } catch (error) {
        console.error('Full error:', error)
        errorMessage.value = `Ошибка выполнения: ${error.message}`
    } finally {
        isButtonDisabled.value = false
    }
}
</script>

<template>
    <div class="code-form">
        <textarea ref="editor"></textarea>
    </div>

    <div class="solution">
        <button 
            class="btn btn-sm btn-outline-primary" 
            @click="send_task_to_run" 
            :disabled="isButtonDisabled"
        >
            {{ isButtonDisabled ? 'Выполнение...' : 'Запустить' }}
        </button>
        <a class="btn btn-sm btn-outline-secondary" href="#task-description">Перейти к условию</a>
        <button class="btn btn-outline-info btn-sm" @click="toggleInfo">
            {{ showInfo ? 'Скрыть информацию' : 'О выполнение кода' }}
        </button>

        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>

        <!-- Обновленный блок отображения результатов -->
        <div v-if="testResult" class="test-result">
            <div :class="['result-alert', testResult.res ? 'alert-success' : 'alert-danger']">
                {{ testResult.res ? '✅ Тест пройден' : '❌ Тест не пройден' }}
                <div class="execution-time" v-if="testResult.completed_time">
                    Время выполнения: {{ testResult.completed_time.toFixed(2) }} сек
                </div>
            </div>
        </div>

        <div v-if="showInfo" class="modal-backdrop" @click="toggleInfo">
            <div class="modal-content" @click.stop>
                <h6>📌 Условия выполнения</h6>
                <p>Решите задачу, ответ нужно вывести в консоль.</p>
                <p>Разрешённые библиотеки: <b>itertools</b></p>
                <p>Уложитесь в лимит по времени</p>
                <p>Версия python: 3.12.5</p>
                <button class="btn btn-danger btn-sm" @click="toggleInfo">Закрыть</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Добавьте эти стили */
.test-result {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 4px;
}

.alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
}

.alert-danger {
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
}

.execution-time {
    margin-top: 0.5rem;
    font-size: 0.9em;
    opacity: 0.8;
}
.code-form {
    margin-top: 15px;
}

.solution {
    margin-top: 10px;
}

.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

/* Окно */
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    max-width: 400px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>