<template>
  <div class="task-admin">
    <!-- Внутренние вкладки для задач -->
    <div class="task-tabs">
      <button
        v-for="action in actions"
        :key="action"
        class="task-tab"
        :class="{ active: activeAction === action }"
        @click="activeAction = action"
      >
        {{ actionLabels[action] }}
      </button>
    </div>

    <!-- Контент вкладок -->
    <div class="task-content">
      <!-- Компонент добавления задачи -->
      <TaskAdd v-if="activeAction === 'create'" />

      <!-- Компонент редактирования задачи -->
      <TaskEdit v-if="activeAction === 'edit'" />

      <!-- Компонент удаления задачи -->
      <TaskDelete v-if="activeAction === 'delete'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import TaskAdd from "./TaskAdmin/TaskAdd.vue";
import TaskEdit from "./TaskAdmin/TaskEdit.vue";
import TaskDelete from "./TaskAdmin/TaskDelete.vue";

const activeAction = ref("create");

const actions = ["create", "edit", "delete"];
const actionLabels = {
  create: "Добавить задачу",
  edit: "Редактировать задачу",
  delete: "Удалить задачу",
};
</script>

<style scoped>
.task-admin {
  padding: 1rem;
}

.task-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.task-tab {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #e9ecef;
  }

  &.active {
    background: #3b82f6;
    color: white;
  }
}

.task-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style>
