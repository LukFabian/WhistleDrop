<template>
  <v-container>
    <h1>Download Encrypted Files</h1>
    <v-btn color="primary" @click="fetchFiles">Fetch Files</v-btn>
    <v-list v-if="files.length">
      <v-list-item
        v-for="file in files"
        :key="file.upload_id"
        :title="'Download ' + file.upload_id"
        @click="downloadFile(file.upload_id)"
      />
    </v-list>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const files = ref([])

const fetchFiles = async () => {
  const token = localStorage.getItem('jwt')
  const res = await axios.get('/files', {
    headers: { Authorization: `Bearer ${token}` }
  })
  files.value = res.data
}

const downloadFile = async (uploadId) => {
  const token = localStorage.getItem('jwt')
  const res = await axios.get(`/download/${uploadId}`, {
    responseType: 'blob',
    headers: { Authorization: `Bearer ${token}` }
  })

  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `${uploadId}.zip`)
  document.body.appendChild(link)
  link.click()
}
</script>
