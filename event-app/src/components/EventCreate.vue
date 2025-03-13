<template>
    <v-container>
        <v-card class="mx-auto" max-width="600">
            <v-card-title class="text-h5">Create New Event</v-card-title>

            <v-card-text>
                <v-form ref="form" lazy-validation>
                    <v-text-field
                        v-model="event.title"
                        label="Event Title"
                        required
                        :rules="[rules.required]"
                    ></v-text-field>

                    <v-text-field
                        v-model="event.organizer"
                        label="Organizer"
                        required
                        :rules="[rules.required]"
                    ></v-text-field>

                    <!-- Fixed Date Picker -->
                    <v-menu
                        v-model="menu"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                                v-model="formattedDate"
                                label="Date"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                                required
                                :rules="[rules.required]"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                            v-model="event.date"
                            @update:modelValue="updateDate"
                            :max="maxDate"
                        ></v-date-picker>
                    </v-menu>

                    <v-textarea
                        v-model="event.description"
                        label="Description"
                        required
                        :rules="[rules.required]"
                    ></v-textarea>
                </v-form>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey" @click="resetForm">Reset</v-btn>
                <v-btn
                    color="primary"
                    :disabled="loading"
                    :loading="loading"
                    @click="createNewEvent"
                >
                    Create Event
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import { ref, computed } from "vue";
import { createEvent } from "../services/eventService";

export default {
    setup(_, { emit }) {
        const event = ref({
            title: "",
            organizer: "",
            date: null,
            description: "",
        });

        const form = ref(null);
        const loading = ref(false);
        const menu = ref(false);
        const maxDate = ref(new Date().toISOString().split("T")[0]);

        const formattedDate = computed(() => {
            return event.value.date
                ? new Date(event.value.date).toLocaleDateString()
                : "";
        });

        const rules = {
            required: (value) => !!value || "This field is required",
        };

        const updateDate = (date) => {
            event.value.date = date;
            menu.value = false; // Close menu after selecting date
        };

        const createNewEvent = async () => {
            const isValid = await form.value.validate();
            if (!isValid) return;

            loading.value = true;
            try {
                const eventData = {
                    ...event.value,
                    date: event.value.date
                        ? new Date(event.value.date).toISOString().split("T")[0]
                        : null,
                };

                const newEvent = await createEvent(eventData);
                emit("eventCreated", newEvent);
                resetForm();
            } catch (error) {
                console.error("Error creating event:", error);
            } finally {
                loading.value = false;
            }
        };

        const resetForm = () => {
            form.value?.reset();
            event.value = {
                title: "",
                organizer: "",
                date: null,
                description: "",
            };
            menu.value = false; // Reset menu state
        };

        return {
            event,
            form,
            rules,
            createNewEvent,
            resetForm,
            loading,
            menu,
            formattedDate,
            maxDate,
            updateDate,
        };
    },
};
</script>
