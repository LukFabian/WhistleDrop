<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn v-if="!auth.isAuthenticated" @click="goToLogin">Journalist Login</v-btn>
        <v-btn v-if="!auth.isAuthenticated" @click="goToRegistration">Journalist Register</v-btn>

        <div v-if="auth.isAuthenticated">
          Logged in as: <strong>{{ auth.userEmail }}</strong>
          <v-btn color="error" @click="auth.logout()" class="ml-2">Logout</v-btn>
          <v-btn color="primary" class="ml-2" :to="'/download'">
            View My Files
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <UploadWhistle></UploadWhistle>
</template>

<script lang="ts" setup>
import {useRouter} from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'
import { jwtDecode } from "jwt-decode";

const router = useRouter()
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // Routes that require auth
  const protectedRoutes = ['/download']

  if (protectedRoutes.includes(to.path)) {
    if (!token) {
      return next('/login')
    }

    try {
      const decoded: any = jwtDecode(token)
      const now = Date.now() / 1000

      if (decoded.exp && decoded.exp < now) {
        // Token expired
        console.warn('Token expired')
        localStorage.removeItem('token')
        return next('/login')
      }
    } catch (e) {
      console.warn('Invalid token', e)
      localStorage.removeItem('token')
      return next('/login')
    }
  }

  next()
})

const auth = useAuthStore()

onMounted(() => {
  auth.loadFromStorage()
})

const goToLogin = () => {
  router.push('/login')
}
const goToRegistration = () => {
  router.push('/register')
}
</script>
