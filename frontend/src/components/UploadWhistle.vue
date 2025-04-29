<template>
  <v-container class="py-10">
    <v-card class="mx-auto" max-width="600">
      <v-card-title>Upload File to WhistleDrop</v-card-title>

      <v-card-text>
        <v-form ref="form">
          <v-file-input
            v-model="file"
            label="Select File"
            accept=".pdf,.doc,.docx,.txt"
            prepend-icon="mdi-upload"
            :rules="[fileRequired]"
          />

          <v-btn
            :loading="loading"
            :disabled="!file || loading"
            color="primary"
            class="mt-4"
            @click="uploadFile"
          >
            Upload
          </v-btn>

          <v-alert
            v-if="uploadSuccess"
            type="success"
            class="mt-4"
            border="start"
          >
            File uploaded successfully!
          </v-alert>

          <v-alert
            v-if="error"
            type="error"
            class="mt-4"
            border="start"
          >
            {{ error }}
          </v-alert>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { uploadApi } from '@/plugins' // <-- Import your generated API client

// States
const file = ref<File | null>(null)
const loading = ref(false)
const uploadSuccess = ref(false)
const error = ref('')


// Simple file required rule
const fileRequired = (value: File | null) => !!value || 'File is required'

// Upload function
const uploadFile = async () => {
  if (!file.value) return

  loading.value = true
  uploadSuccess.value = false
  error.value = ''

  try {
    const response = await uploadApi.uploadUploadFile(file.value)

    if (response.status === 200 && response.data.status === 'success') {
      uploadSuccess.value = true
      file.value = null
    } else {
      throw new Error('Upload failed')
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Unknown error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.v-file-input {
  margin-bottom: 20px;
}
</style>
