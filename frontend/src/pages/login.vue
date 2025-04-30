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
import {useAuthStore} from "@/stores/auth.js";

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const login = async () => {
  try {
    await auth.login(email.value, password.value)
    await router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed'
  }
}

</script>
