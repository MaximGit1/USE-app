<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const isAuthenticated = ref(false); // Состояние аутентификации

// Функция для проверки аутентификации
const checkAuth = async () => {
  try {
    const response = await axios.post(
      "https://127.0.0.1/api/v1/auth/check/",
      {},
      { withCredentials: true }
    );
    if (response.data === true) {
      isAuthenticated.value = true; // Обновляем состояние, если ответ сервера - true
    } else {
      isAuthenticated.value = false; // В другом случае - false
    }
  } catch (error) {
    console.error("Ошибка при проверке аутентификации", error);
    isAuthenticated.value = false; // Ошибка - не аутентифицирован
  }
};

// Выход пользователя
const logout = async () => {
  try {
    await axios.post(
      "https://127.0.0.1:8000/auth/logout/",
      {},
      { withCredentials: true }
    );
    isAuthenticated.value = false;
    router.push("/");
  } catch (error) {
    console.error("Ошибка при выходе", error);
  }
};

// Инициализация
onMounted(() => {
  checkAuth(); // Проверяем аутентификацию при монтировании компонента
  window.addEventListener("auth-change", checkAuth); // Проверка аутентификации при изменении события
});
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/">Задачи</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/theory"
              >Теория</a
            >
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Я
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">Профиль</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li v-if="!isAuthenticated">
                <a class="dropdown-item" href="/login">Войти</a>
              </li>
              <li v-if="isAuthenticated">
                <a class="dropdown-item" href="#" @click="logout">Выйти</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
