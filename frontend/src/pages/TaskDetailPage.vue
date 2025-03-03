<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import TaskDetail from "../components/TaskDetail.vue";
import TaskEditor from "../components/TaskEditor.vue";

const route = useRoute();
const router = useRouter();
const task = ref(null);
const showInfo = ref(false);

const toggleInfo = () => {
  showInfo.value = !showInfo.value;
};

const apiUrl = import.meta.env.VITE_API_URL;
const authVerifyUser = apiUrl + "/auth/verify-role/";

async function checkPermission() {
  try {
    const response = await fetch(authVerifyUser, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        role: "user",
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data; // Возвращаем ответ сервера как есть
  } catch (error) {
    console.error("Error checking permissions:", error);
    return false;
  }
}

onMounted(async () => {
  try {
    // Проверка прав доступа
    const hasAccess = await checkPermission();
    if (hasAccess !== true) {
      // Проверяем строгое равенство
      router.push("/403"); // Перенаправление на страницу "Доступ запрещен"
      return;
    }

    // Загрузка данных задачи
    const taskId = route.params.taskId;
    const taskDetail = apiUrl + `/tasks/base/${taskId}`;

    if (history.state?.id) {
      task.value = history.state;
    } else {
      const response = await fetch(taskDetail);
      if (!response.ok) throw new Error("Ошибка загрузки данных");
      const data = await response.json();

      task.value = {
        id: data.id,
        type: data.type,
        body: data.body,
        timeLimit: data.time_limit,
      };
    }
  } catch (error) {
    console.error("Ошибка:", error);
    router.push("/403"); // Перенаправление на страницу "Доступ запрещен"
  }
});
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
