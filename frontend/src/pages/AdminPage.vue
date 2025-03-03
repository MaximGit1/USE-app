<template>
  <div class="admin-page">
    <!-- Верхняя панель с вкладками -->
    <div class="admin-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="nav-button"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
      </button>
    </div>

    <!-- Контент вкладок -->
    <div class="admin-content">
      <Analytics v-if="activeTab === 'analytics'" />
      <TaskAdmin v-if="activeTab === 'tasks'" />
      <UserAdmin v-if="activeTab === 'users'" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Analytics from "../components/admin/Analytics.vue";
import TaskAdmin from "../components/admin/TaskAdmin.vue";
import UserAdmin from "../components/admin/UserAdmin.vue";

const router = useRouter();
const activeTab = ref("analytics");

const tabs = [
  { id: "analytics", label: "Аналитика", icon: "bi bi-bar-chart" },
  { id: "tasks", label: "Задачи", icon: "bi bi-list-task" },
  { id: "users", label: "Пользователи", icon: "bi bi-people" },
];

const apiUrl = import.meta.env.VITE_API_URL;
const authVerifyAdmin = apiUrl + "/auth/verify-role/";
async function checkPermission() {
  try {
    const response = await fetch(authVerifyAdmin, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        role: 'admin'
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;  // Возвращаем ответ сервера как есть
  } catch (error) {
    console.error('Error checking permissions:', error);
    return false;
  }
}

onMounted(async () => {
  try {
    const hasAccess = await checkPermission();
    if (hasAccess !== true) {  // Проверяем строгое равенство
      router.push('/403');  // Перенаправление на страницу "Доступ запрещен"
    }
  } catch (error) {
    console.error('Ошибка:', error);
    router.push('/login');  // Перенаправление на страницу входа
  }
});
</script>

<style scoped>
.admin-page {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.admin-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.nav-button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background: white;
  color: #495057;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  }

  &.active {
    background: #3b82f6;
    color: white;
  }
}

.admin-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}
</style>
