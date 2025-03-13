<template>
    <v-dialog v-model="dialog" persistent max-width="500px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{
                    isEditing ? "Edit Event" : "Create Event"
                }}</span>
            </v-card-title>

            <v-card-text>
                <v-form ref="eventForm">
                    <v-text-field
                        v-model="event.title"
                        label="Event Title"
                        :rules="[(v) => !!v || 'Title is required']"
                        required
                    ></v-text-field>

                    <v-menu
                        v-model="datePicker"
                        :close-on-content-click="false"
                    >
                        <template v-slot:activator="{ props }">
                            <v-text-field
                                v-bind="props"
                                v-model="formattedDate"
                                label="Event Date"
                                readonly
                            ></v-text-field>
                        </template>
                        <v-date-picker v-model="event.date"></v-date-picker>
                    </v-menu>

                    <v-select
                        v-model="event.organizer"
                        :items="organizers"
                        label="Organizer"
                    ></v-select>

                    <v-textarea
                        v-model="event.description"
                        label="Description"
                    ></v-textarea>
                </v-form>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey" @click="closeDialog">Cancel</v-btn>
                <v-btn color="primary" :loading="loading" @click="saveEvent"
                    >Save</v-btn
                >
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { ref, computed, watch, defineProps, defineEmits, onMounted } from "vue";
import {
    getOrganizers,
    createEvent,
    updateEvent,
} from "../services/eventService";
import { format } from "date-fns"; // Ensure you install: npm install date-fns

export default {
    props: {
        modelValue: Boolean,
        eventData: Object,
    },
    setup(props, { emit }) {
        const dialog = ref(false);
        const isEditing = ref(false);
        const loading = ref(false);
        const datePicker = ref(false);
        const organizers = ref([]);
        const event = ref({
            title: "",
            date: "",
            organizer: "",
            description: "",
        });

        const eventForm = ref(null);

        // Sync dialog with modelValue
        watch(
            () => props.modelValue,
            (newVal) => {
                dialog.value = newVal;
            }
        );

        // Watch for incoming eventData and populate form
        watch(
            () => props.eventData,
            (newEvent) => {
                if (newEvent) {
                    event.value = { ...newEvent };
                    isEditing.value = true;
                } else {
                    isEditing.value = false;
                }
            },
            { immediate: true }
        );

        // Fetch organizers from API
        const fetchOrganizers = async () => {
            try {
                organizers.value = await getOrganizers();
            } catch (error) {
                console.error("Error fetching organizers:", error);
            }
        };

        // Compute formatted date
        const formattedDate = computed(() =>
            event.value.date
                ? format(new Date(event.value.date), "yyyy-MM-dd")
                : ""
        );

        const closeDialog = () => {
            dialog.value = false;
            emit("update:modelValue", false);
        };

        const saveEvent = async () => {
            const { valid } = await eventForm.value.validate();
            if (!valid) return;

            loading.value = true;
            try {
                if (isEditing.value) {
                    await updateEvent(event.value.id, event.value);
                } else {
                    await createEvent(event.value);
                }
                emit("event-saved");
                closeDialog();
            } catch (error) {
                console.error("Error saving event:", error);
            } finally {
                loading.value = false;
            }
        };

        onMounted(fetchOrganizers);

        return {
            dialog,
            isEditing,
            loading,
            datePicker,
            organizers,
            event,
            formattedDate,
            eventForm,
            closeDialog,
            saveEvent,
        };
    },
};
</script>
