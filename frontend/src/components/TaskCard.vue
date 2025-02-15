<script setup>
import MarkdownRenderer from './MarkdownRenderer.vue';

defineProps({
    id: Number,
    type: Number,
    body: String,
    timeLimit: Number
})
</script>

<template>
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Тип {{ type }} <b class="text-info">№{{ id }}</b></h5>
            </div>
            <div class="card-body">
            <MarkdownRenderer :content="body" />
            <p class="text-danger">Лимит: {{ timeLimit }}</p>
            </div>
        </div>

</template>

<style setup>
.card {
    margin-top: 3%;
}
</style>