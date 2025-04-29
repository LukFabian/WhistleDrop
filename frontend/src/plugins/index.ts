/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify'
import router from '../router'

// Types
import type { App } from 'vue'
import {Configuration, UploadApi} from "@/generated";
import { http } from '@/lib/http';

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(router)
}

const config = new Configuration({
  basePath: '',                 // leave empty – we hand the baseURL via axios
});

export const uploadApi = new UploadApi(config, undefined, http);
