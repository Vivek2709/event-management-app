import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import vuetify from "./plugins/vuetify"; // Import Vuetify setup
import router from "./router";
import "vuetify/styles"; // Ensure styles are included

const app = createApp(App).use(vuetify).use(router).mount("#app");
