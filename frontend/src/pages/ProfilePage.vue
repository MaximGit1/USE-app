<template>
  <div class="container py-4">
    <!-- Лоадер -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Основной контент -->
    <div v-else-if="user" class="profile-container">
      <!-- Заголовок профиля -->
      <div class="d-flex align-items-center mb-4">
        <h1 :class="roleClass" class="me-3">{{ user.username }}</h1>
        <div class="status-indicator" :class="statusClass"></div>
      </div>

      <!-- Дополнительная информация -->
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Информация о пользователе</h5>
          <ul class="list-group list-group-flush">
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <span>Роль:</span>
              <span :class="roleClass" class="badge rounded-pill">
                {{ user.role }}
              </span>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <span>Статус:</span>
              <span :class="statusClass">
                {{ user.is_active ? "Активен ✓" : "Неактивен ✗" }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <h2 v-if="stats.length > 0" class="text-center">Статистика выполнения</h2>
    <div class="tasks-container">
      <TaskStatCard
        v-for="task in stats"
        :key="task.number"
        :taskNumber="task.number"
        :taskCompletion="task.percent"
      />
    </div>
    <div v-if="!loading && stats.length === 0" class="text-center text-muted">
      Нет данных о выполнении заданий
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import TaskStatCard from "../components/profileStats/TaskStatCard.vue";

const router = useRouter();
const user = ref(null);
const stats = ref([]);
const loading = ref(true);
const errorMessage = ref("");
let timeoutId = null;
const controller = new AbortController();

// Вычисляемые свойства для стилей
const roleClass = computed(() => ({
  "text-primary": user.value?.role === "admin",
  "text-success": user.value?.role === "moderator",
  "text-warning": user.value?.role === "premium",
  "text-dark": !user.value?.role || user.value?.role === "user",
}));

const statusClass = computed(() => (
  user.value?.is_active
    ? "text-success bg-success-light"
    : "text-danger bg-danger-light"
));

const fetchUserId = async () => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/auth/my-id/`,
      {
        method: "POST",
        credentials: "include",
        signal: controller.signal,
      }
    );

    if (!response.ok) {
      if (response.status === 401 || response.status === 403) {
        router.push("/login");
      }
      throw new Error("Ошибка авторизации");
    }

    const { user_id } = await response.json();
    return user_id;
  } catch (error) {
    handleError(error);
    return null;
  }
};

const fetchUserData = async (userId) => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/users/${userId}`,
      {
        signal: controller.signal,
      }
    );

    if (!response.ok) {
      if (response.status === 403) {
        router.push("/login");
      }
      throw new Error("Пользователь не найден");
    }

    user.value = await response.json();
    console.log("Данные пользователя:", user.value); // Для отладки
  } catch (error) {
    handleError(error);
  }
};

const fetchStats = async (userId) => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/stats/profile/${userId}/`,
      {
        signal: controller.signal,
      }
    );

    if (!response.ok) {
      throw new Error("Не удалось загрузить статистику");
    }

    const data = await response.json();
    stats.value = data.map(task => ({
      number: task.task_type,
      percent: task.completed_percent
    }));
  } catch (error) {
    handleError(error);
  }
};

const handleError = (error) => {
  console.error(error);
  if (error.name !== "AbortError") {
    errorMessage.value = error.message;
    loading.value = false;
    router.push("/login");
  }
};

onMounted(async () => {
  timeoutId = setTimeout(() => {
    if (loading.value) {
      controller.abort();
      router.push("/login");
    }
  }, 3000);

  try {
    const userId = await fetchUserId();
    if (userId) {
      await fetchUserData(userId);
      await fetchStats(userId);
    }
    clearTimeout(timeoutId);
  } catch (error) {
    handleError(error);
    clearTimeout(timeoutId);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.status-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.bg-success-light {
  background-color: rgba(40, 167, 69, 0.1);
}

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.1);
}

.badge {
  padding: 0.5em 1em;
  border: 1px solid currentColor;
}

.list-group-item {
  transition: background-color 0.2s;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.tasks-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 1rem;
  justify-content: center;
}
</style>
