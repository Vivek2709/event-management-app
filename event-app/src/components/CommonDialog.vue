<template>
    <v-dialog v-model="isVisible" :width="width">
        <v-card>
            <v-card-title class="text-h6">
                {{ title }}
            </v-card-title>
            <v-card-text>
                <slot></slot>
            </v-card-text>
            <v-card-actions class="justify-end">
                <v-btn variant="text" @click="$emit('close')">Cancel</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    props: {
        title: { type: String, required: true },
        modelValue: { type: Boolean, required: true },
        width: { type: String, default: "auto" },
    },
    computed: {
        isVisible: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit("update:modelValue", value);
            },
        },
    },
};
</script>
