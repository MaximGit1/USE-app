<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

// Данные формы
const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

// Функция входа
const login = async () => {
  errorMessage.value = "";
  isLoading.value = true;

  try {
    const response = await axios.post(
      "https://127.0.0.1:8000/auth/login/",
      {
        username: username.value,
        password: password.value,
      },
      { withCredentials: true }
    ); // Обязательно для работы с куками!

    if (response.status === 200) {
      alert("Успешный вход!");
      router.push("/"); // Перенаправляем пользователя
      // Диспетчеризация события для обновления статуса в HeaderMenu.vue
      window.dispatchEvent(new Event("auth-change"));
      // Или вызвать checkAuth() напрямую:
      checkAuth();
    }
  } catch (error) {
    errorMessage.value =
      error.response?.status === 401
        ? "Ошибка авторизации. Проверьте логин и пароль."
        : "Ошибка сервера. Попробуйте позже.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <form @submit.prevent="login" class="login-form">
    <div class="form-group">
      <label for="username">Имя пользователя</label>
      <input
        type="text"
        class="form-control"
        id="username"
        v-model="username"
        placeholder="Введите логин"
        required
      />
    </div>
    <div class="form-group">
      <label for="password">Пароль</label>
      <input
        type="password"
        class="form-control"
        id="password"
        v-model="password"
        placeholder="Введите пароль"
        required
      />
    </div>
    <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
      {{ isLoading ? "Вход..." : "Войти" }}
    </button>
    <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
  </form>
</template>

<style scoped>
.login-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  background: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
</style>
