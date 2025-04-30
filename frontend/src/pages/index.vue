<template>
  <v-container>
    <v-btn color="primary" @click="goToLogin">
      Journalist Login
    </v-btn>
  </v-container>
  <v-container>
    <v-btn color="secondary" @click="goToRegistration">
      Journalist Registration
    </v-btn>
  </v-container>
  <UploadWhistle></UploadWhistle>
</template>

<script lang="ts" setup>
import {useRouter} from 'vue-router'

const router = useRouter()
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('jwt')

  if (to.path === '/download' && !token) {
    next('/login')
  } else {
    next()
  }
})
const goToLogin = () => {
  router.push('/login')
}
const goToRegistration = () => {
  router.push('/register')
}
</script>
