<template>
  <v-container>
    <v-row justify="space-between" align="center" class="mb-4">
      <v-col>
        <h2>My Uploaded Files</h2>
      </v-col>
      <v-col class="text-right">
        Logged in as: <strong>{{ auth.userEmail }}</strong>
      </v-col>
      <v-btn color="error" @click="handleLogout()" class="ml-2">Logout</v-btn>
    </v-row>

    <v-alert v-if="error" type="error" class="mb-4">
      {{ error }}
    </v-alert>

    <v-card v-if="files.length === 0" class="pa-4">
      No uploaded files found.
    </v-card>

    <v-row>
      <v-col v-for="file in files" :key="file.upload_id" cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>
            {{ file.filename }}
          </v-card-title>
          <v-card-subtitle>
            File ID: {{ file.upload_id }}
          </v-card-subtitle>
          <v-card-text>
            Preview: <small>{{ file.decrypted_preview }}</small>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="downloadFile(file.filename, file.upload_id)" color="primary">Download</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {downloadApi, uploadApi} from '@/plugins'
import {useRouter} from 'vue-router'

const files = ref<any[]>([])
const error = ref<string | null>(null)
const router = useRouter()
const auth = useAuthStore()

const fetchFiles = async () => {
  try {
    const response = await uploadApi.uploadGetMyUploads()
    files.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to fetch files'
  }
}

const handleLogout = () => {
  auth.logout()
  router.push('/')
}

const downloadFile = async (fileName: string, uploadId: string) => {
  try {
    const response = await downloadApi.downloadDownloadFile(uploadId, {
      responseType: 'blob',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })

    // Force browser download
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    if (fileName.startsWith("decrypted_") && fileName.endsWith(".bin")) {
      link.setAttribute('download', `file_${uploadId}`)
    } else {
      link.setAttribute('download', fileName)
    }
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (err: any) {
    console.error('Download failed', err)
    error.value = 'Failed to download file'
  }
}

onMounted(() => {
  fetchFiles()
})
</script>
