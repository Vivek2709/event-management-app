import { createVuetify } from "vuetify";
import * as components from "vuetify/components"; // Import ALL components
import * as directives from "vuetify/directives"; // Import ALL directives
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

export default createVuetify({
    components,
    directives,
    icons: {
        defaultSet: "mdi",
    },
    theme: {
        defaultTheme: "eventTheme",
        themes: {
            eventTheme: {
                dark: false,
                colors: {
                    primary: "#1E88E5",
                    secondary: "#FBC02D",
                    accent: "#7B1FA2",
                    background: "#F5F7FA",
                    surface: "#FFFFFF",
                    text: "#333333",
                    error: "#E53935",
                },
            },
        },
    },
});
