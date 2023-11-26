
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PROJECT_NAME: string | ""
  readonly VITE_BACKEND_HOST: string | null
  readonly VITE_DEBUG_BACKEND_HOST: string | null
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}