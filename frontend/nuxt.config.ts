// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: [
        "nuxt-bootstrap-icons",
    ],
    css: [
        "~/node_modules/bootstrap/dist/css/bootstrap.css",
    ],
    plugins: [
        {src: "~/plugins/jquery.js", mode: "client"},
    ],
})