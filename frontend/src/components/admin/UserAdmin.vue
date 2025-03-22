<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";

const apiUrl = import.meta.env.VITE_API_URL;
const users = ref([]);
const isLoading = ref(false);
const errorMessage = ref("");
const searchQuery = ref("");
const toast = useToast();

const roles = ["USER", "MODERATOR", "ADMIN"];

// Пагинация
const currentPage = ref(1);
const totalUsers = ref(0);
const limit = 10;

// Функция получения общего числа пользователей
const fetchTotalUsers = async () => {
  try {
    const response = await axios.get(`${apiUrl}/users/`, {
      params: { offset: 0, limit: 1, order_by: "id", sortorder: "desc" },
    });

    if (response.data.length > 0) {
      totalUsers.value = response.data[0].user_id;
    } else {
      totalUsers.value = 0;
    }
  } catch (error) {
    totalUsers.value = 0;
    errorMessage.value = "Ошибка получения общего числа пользователей.";
  }
};

// Функция загрузки пользователей
const fetchUsers = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  if (totalUsers.value === 0) await fetchTotalUsers(); // Убедимся, что totalUsers обновлён

  try {
    const response = await axios.get(`${apiUrl}/users/`, {
      params: {
        offset: (currentPage.value - 1) * limit,
        limit: limit,
        order_by: "id",
        sortorder: "asc",
      },
    });

    users.value = response.data.map((user) => ({
      ...user,
      role: user.role.toUpperCase(),
    }));
  } catch (error) {
    errorMessage.value = "Ошибка загрузки пользователей.";
  } finally {
    isLoading.value = false;
  }
};

// Поиск пользователя
const searchUser = async () => {
  if (!searchQuery.value.trim()) {
    fetchUsers();
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await axios.get(`${apiUrl}/users/username/${searchQuery.value}`);
    users.value = [response.data];
  } catch (error) {
    errorMessage.value = "Пользователь не найден.";
  } finally {
    isLoading.value = false;
  }
};

// Обновление роли пользователя
const updateRole = async (user) => {
  try {
    await axios.patch(`${apiUrl}/users/${user.user_id}/update/role`, { role: user.role.toLowerCase() });
    toast.success(`Роль пользователя ${user.username} успешно обновлена!`);
  } catch (error) {
    toast.error("Ошибка обновления роли.");
  }
};

// Обновление статуса пользователя
const updateStatus = async (user) => {
  if (!user.user_id) {
    errorMessage.value = "Ошибка: отсутствует ID пользователя.";
    return;
  }

  try {
    await axios.patch(
      `${apiUrl}/users/${user.user_id}/update/status/?is_active=${user.is_active}`, // ✅ query-param
      {},
      {
        headers: {
          "Content-Type": "application/json",
        }
      }
    );
    toast.success(`Статус пользователя ${user.username} успешно обновлён!`);
  } catch (error) {
    toast.error("Ошибка обновления статуса.");
  }
};

// Функции переключения страниц
const totalPages = () => Math.max(1, Math.ceil(totalUsers.value / limit));

const nextPage = () => {
  if (currentPage.value < totalPages()) {
    currentPage.value++;
    fetchUsers();
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchUsers();
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div class="user-admin">
    <h2>Управление пользователями</h2>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>

    <!-- Форма поиска -->
    <div class="search-container">
      <input v-model="searchQuery" type="text" placeholder="Поиск по имени..." class="form-control" />
      <button @click="searchUser" class="btn btn-primary">Поиск</button>
    </div>

    <table class="table" v-if="!isLoading">
      <thead>
        <tr>
          <th>ID</th>
          <th>Никнейм</th>
          <th>Роль</th>
          <th>Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.user_id">
          <td>{{ user.user_id }}</td>
          <td>{{ user.username }}</td>
          <td>
            <select v-model="user.role" @change="updateRole(user)" class="form-select">
              <option v-for="role in roles" :key="role" :value="role">
                {{ role }}
              </option>
            </select>
          </td>
          <td>
            <input type="checkbox" v-model="user.is_active" @change="updateStatus(user)" />
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="isLoading">Загрузка пользователей...</p>

    <!-- Пагинация -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn btn-secondary">Назад</button>
      <span>Страница {{ currentPage }} / {{ totalPages() }}</span>
      <button @click="nextPage" :disabled="currentPage >= totalPages()" class="btn btn-secondary">
        Вперёд
      </button>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
</style>
