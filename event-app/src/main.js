import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import vuetify from "./plugins/vuetify"; // Import Vuetify setup
import router from "./router";
import "vuetify/styles";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import "@mdi/font/css/materialdesignicons.css"; // Ensure styles are included

// const vuetify = createVuetify({
//     icons: {
//         defaultSet: "mdi",
//     },
// });
const app = createApp(App).use(vuetify).use(router);

app.component("VueDatePicker", VueDatePicker);

app.mount("#app");
