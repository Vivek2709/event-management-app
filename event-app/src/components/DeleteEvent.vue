<template>
    <v-dialog :model-value="modelValue" max-width="400px">
        <v-card>
            <v-card-title class="text-h6"> Delete Event </v-card-title>
            <v-card-text>
                Are you sure you want to delete this event?
            </v-card-text>
            <v-card-actions>
                <v-spacer />
                <v-btn color="grey" @click="closeDialog"> Cancel </v-btn>
                <v-btn color="red" @click="deleteEvent"> Delete </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
    modelValue: Boolean, // Instead of v-model
    eventId: Number,
});

const emit = defineEmits(["update:modelValue", "event-deleted"]);

const closeDialog = () => {
    emit("update:modelValue", false);
};

const deleteEvent = () => {
    console.log("Deleting event:", props.eventId);
    emit("event-deleted", props.eventId);
    closeDialog();
};
</script>
