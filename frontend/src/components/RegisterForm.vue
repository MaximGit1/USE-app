<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const apiUrl = import.meta.env.VITE_API_URL;
const authRegister = apiUrl + "/auth/register/";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const register = async () => {
  errorMessage.value = "";
  isLoading.value = true;

  try {
    const response = await axios.post(authRegister, {
      username: username.value,
      password: password.value,
    });

    if (response.status === 201) {
      alert("Регистрация успешна! Перенаправление на страницу входа.");
      router.push("/login");
    }
  } catch (error) {
    errorMessage.value =
      error.response?.status === 401
        ? "Ошибка авторизации. Попробуйте снова."
        : "Ошибка сервера. Попробуйте позже.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <form @submit.prevent="register" class="register-form">
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
      {{ isLoading ? "Регистрация..." : "Зарегистрироваться" }}
    </button>
    <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
    <p class="mt-2">Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
  </form>
</template>

<style scoped>
.register-form {
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
