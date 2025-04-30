<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-6 rounded-xl">
          <v-card-title class="text-h5 font-weight-bold">Journalist Registration</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="register" ref="formRef" v-model="formValid">
              <v-text-field
                v-model="email"
                label="Email"
                :rules="emailRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                :rules="passwordRules"
                required
              ></v-text-field>

              <v-btn :disabled="!formValid" type="submit" color="primary" class="mt-4" block>
                Register
              </v-btn>

              <v-alert
                v-if="success"
                type="success"
                class="mt-4"
              >
                Registration successful. Await admin activation.
              </v-alert>

              <v-alert
                v-if="error"
                type="error"
                class="mt-4"
              >
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {ref} from 'vue'
import axios from 'axios'
import {registerApi} from "@/plugins/index.js";

const email = ref('');
const password = ref('');
const formRef = ref(null);
const formValid = ref(false);
const success = ref(false);
const error = ref('');

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid',
]

const passwordRules = [
  v => !!v || 'Password is required',
  v => v.length >= 8 || 'Password must have at least 8 characters',
  v => /[A-Z]/.test(v) || 'Password must have at least one uppercase letter',
  v => /[a-z]/.test(v) || 'Password must have at least one lowercase letter',
  v => /[0-9]/.test(v) || 'Password must have at least one digit',
]

const register = async () => {
  if (!formValid.value) return

  error.value = ''
  success.value = false

  try {
    const journalist = {
      email: email.value,
      password: password.value,
    };
    await registerApi.registerRegisterJournalist(journalist)
    success.value = true
    email.value = ''
    password.value = ''
    formRef.value.reset()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed.'
  }
}
</script>
