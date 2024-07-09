import $ from "jquery";
import * as bootstrap from "bootstrap";

export default defineNuxtPlugin((nuxtApp) => {
    window.$ = $;
    nuxtApp.$config.public.bootstrap = bootstrap;
})