import { defineStore } from 'pinia'
import axios from 'axios'
import {loginApi} from "@/plugins";

interface AuthState {
  token: string
  userEmail: string
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token') || '',
    userEmail: localStorage.getItem('userEmail') || '',
  }),
  getters: {
    isAuthenticated: (state): boolean => !!state.token,
  },
  actions: {
    async login(email: string, password: string): Promise<void> {
      const response = await loginApi.loginLogin(email, password)
      this.token = response.data.access_token
      this.userEmail = email
      localStorage.setItem('token', this.token)
      localStorage.setItem('userEmail', this.userEmail)
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    },

    logout(): void {
      this.token = ''
      this.userEmail = ''
      localStorage.removeItem('token')
      localStorage.removeItem('userEmail')
      delete axios.defaults.headers.common['Authorization']
    },

    loadFromStorage(): void {
      this.token = localStorage.getItem('token') || ''
      this.userEmail = localStorage.getItem('userEmail') || ''
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    }
  }
})
