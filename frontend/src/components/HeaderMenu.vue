<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const isAuthenticated = ref(false);
const apiUrl = import.meta.env.VITE_API_URL;
const authCheck = apiUrl + "/auth/check/";
const authLogout = apiUrl + "/auth/logout/";

const checkAuth = async () => {
  try {
    const response = await axios.post(authCheck, {}, { withCredentials: true });
    isAuthenticated.value = response.data === true;
  } catch (error) {
    console.error("Ошибка при проверке аутентификации", error);
    isAuthenticated.value = false;
  }
};

const logout = async () => {
  try {
    await axios.post(authLogout, {}, { withCredentials: true });
    isAuthenticated.value = false;
    router.push("/");
  } catch (error) {
    console.error("Ошибка при выходе", error);
  }
};

onMounted(() => {
  checkAuth();
  window.addEventListener("auth-change", checkAuth);
});
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">USE</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Задачи</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/theory">Теория</router-link>
          </li>
        </ul>

        <ul class="navbar-nav ms-auto">
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="userDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-person-circle me-1"></i>Профиль
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <li><router-link class="dropdown-item" to="/profile">Мой профиль</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li v-if="!isAuthenticated">
                <router-link class="dropdown-item" to="/login">Войти</router-link>
              </li>
              <li v-if="isAuthenticated">
                <a class="dropdown-item text-danger" href="#" @click="logout">Выйти</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.25rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: all 0.2s;
}

.nav-link:hover {
  color: var(--bs-primary);
}

.dropdown-menu {
  min-width: 200px;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.dropdown-item {
  padding: 0.5rem 1rem;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.text-danger:hover {
  color: #dc3545 !important;
}

@media (max-width: 767.98px) {
  .navbar-collapse {
    margin-top: 1rem;
  }

  .dropdown-menu {
    border: none;
    box-shadow: none;
  }
}
</style>
