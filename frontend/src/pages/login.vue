<template>
  <v-container class="mt-8">
    <v-card class="pa-6" elevation="4">
      <v-card-title>Journalist Login</v-card-title>
      <v-card-text>
        <v-text-field v-model="email" label="Email" type="email" />
        <v-text-field v-model="password" label="Password" type="password"/>

        <v-btn color="primary" :loading="loading" @click="login">Login</v-btn>

        <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {loginApi} from '@/plugins'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

const login = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await loginApi.loginLogin(email.value, password.value)

    localStorage.setItem('jwt', response.data.access_token)
    router.push('/download')
  } catch (e) {
    error.value = 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
