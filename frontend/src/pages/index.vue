<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn v-if="!auth.isAuthenticated" @click="goToLogin">Journalist Login</v-btn>
        <v-btn v-if="!auth.isAuthenticated" @click="goToRegistration">Journalist Register</v-btn>

        <div v-if="auth.isAuthenticated">
          Logged in as: <strong>{{ auth.userEmail }}</strong>
          <v-btn color="error" @click="auth.logout()" class="ml-2">Logout</v-btn>
          <v-btn color="primary" class="mt-2" :to="'/download'">
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

  if (to.path === '/download') {
    if (!token) {
      next('/login')
    } else {
      try {
        // Decode JWT
        const decoded: { exp: number; sub: string } = jwtDecode(token)

        // Check expiration
        const currentTime = Date.now() / 1000 // in seconds
        if (decoded.exp < currentTime) {
          // Token expired
          localStorage.removeItem('token')
          next('/login')
        } else {
          // Token valid
          next()
        }
      } catch (e) {
        // Invalid token
        console.error('Invalid token', e)
        localStorage.removeItem('token')
        next('/login')
      }
    }
  } else {
    next()
  }
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
