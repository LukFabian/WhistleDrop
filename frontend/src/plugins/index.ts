/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify'
import router from '../router'

// Types
import type {App} from 'vue'
import {LoginApi, Configuration, DownloadApi, RegisterApi, UploadApi} from "@/generated";
import {http} from '@/lib/http';

export function registerPlugins(app: App) {
  app
    .use(vuetify)
    .use(router)
}
let apiBaseUrl: string
if (import.meta.env.MODE === "development") {
  apiBaseUrl = "http://127.0.0.1:8000"
} else {
  apiBaseUrl = "http://127.0.0.1:8000"
}
const config = new Configuration({
  basePath: apiBaseUrl,
});

export const uploadApi = new UploadApi(config, undefined, http);
export const downloadApi = new DownloadApi(config, undefined, http);
export const loginApi = new LoginApi(config, undefined, http);
export const registerApi = new RegisterApi(config, undefined, http);
