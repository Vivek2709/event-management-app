<template>
    <v-btn
        :color="buttonColor"
        :loading="loading"
        :disabled="disabled || loading"
        @click="$emit('click', $event)"
        variant="elevated"
    >
        <slot></slot>
    </v-btn>
</template>

<script>
import { computed } from "vue";

export default {
    props: {
        color: { type: String, default: "primary" },
        loading: { type: Boolean, default: false },
        disabled: { type: Boolean, default: false },
    },
    setup(props) {
        const validColors = [
            "primary",
            "secondary",
            "success",
            "error",
            "warning",
            "info",
        ];
        const buttonColor = computed(() =>
            validColors.includes(props.color) ? props.color : "primary"
        );

        return { buttonColor };
    },
};
</script>
