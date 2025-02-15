import { createRouter, createWebHistory } from 'vue-router'
import TaskListPage from '../pages/TaskListPage.vue'
import TaskDetailPage from '../pages/TaskDetailPage.vue'
import TheoryPage from '../pages/TheoryPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import Error403Page from '../pages/Error403Page.vue'
import AdminPage from '../pages/AdminPage.vue'

const routes = [
    { path: '/', component: TaskListPage },
    { path: '/:taskId/detail', component: TaskDetailPage },
    { path: '/theory', component: TheoryPage },
    { path: '/login', component: LoginPage },
    { path: '/403',  name: 'Error403', component: Error403Page },
    { path: '/admin', component: AdminPage },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
