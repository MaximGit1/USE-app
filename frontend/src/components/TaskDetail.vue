<script setup>
import { computed } from 'vue';
import MarkdownRenderer from './MarkdownRenderer.vue';

const props = defineProps({
    id: Number,
    type: Number,
    body: String,
    timeLimit: Number
});

// Генерация пути к изображению через `new URL()`
const taskImg = computed(() => new URL(`../assets/img/task${props.type}.webp`, import.meta.url).href);
</script>


<template>
    <div class="card mb-3" id="task-description">
        <img :src="taskImg" class="card-img-top" alt="Task image">
        <div class="card-body">
            <h5 class="card-title">Задача <b class="text-info">№{{ id }}</b></h5>
            <MarkdownRenderer :content="body" />
            <p class="text-danger font-weight-bold">Лимит: {{ timeLimit }} секунд</p>
            <p class="card-text"><small class="text-body-secondary">{{ type }} номер задания в ЕГЭ</small></p>
        </div>
    </div>
</template>

<style scoped>
.card {
    margin-top: 1%;
    border-radius: 10px;
    overflow: hidden;
}

.run-info {
    margin-top: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-left: 5px solid #17a2b8;
    border-radius: 8px;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease-in-out;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>
