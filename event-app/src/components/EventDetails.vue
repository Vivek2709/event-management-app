<template>
    <v-dialog v-model="dialog" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ event?.title }}</span>
            </v-card-title>

            <v-card-text>
                <v-list v-if="event">
                    <v-list-item>
                        <v-list-item-title
                            >Date: {{ event.date }}</v-list-item-title
                        >
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>
                            Organizer: {{ event.organizer?.name || "Unknown" }}
                        </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>Description:</v-list-item-title>
                        <v-list-item-subtitle>{{
                            event.description
                        }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>

                <h3 class="mt-4">Attendees</h3>
                <v-list v-if="event?.attendees.length">
                    <v-list-item
                        v-for="(attendee, index) in event.attendees"
                        :key="index"
                    >
                        <v-list-item-content>
                            <v-list-item-title>{{
                                attendee.name
                            }}</v-list-item-title>
                            <v-list-item-subtitle>{{
                                attendee.email
                            }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
                <v-alert v-else type="info" dense>No attendees yet.</v-alert>

                <v-btn color="primary" class="mt-2" @click="addAttendee"
                    >Add Attendee</v-btn
                >
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey" @click="closeDialog">Close</v-btn>
            </v-card-actions>
        </v-card>

        <!-- Add Attendee Dialog -->
        <v-dialog v-model="attendeeDialog" max-width="400px">
            <v-card>
                <v-card-title>Add Attendee</v-card-title>
                <v-card-text>
                    <v-text-field
                        v-model="newAttendee.name"
                        label="Name"
                    ></v-text-field>
                    <v-text-field
                        v-model="newAttendee.email"
                        label="Email"
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" @click="closeAttendeeDialog"
                        >Cancel</v-btn
                    >
                    <v-btn
                        color="primary"
                        :loading="loading"
                        @click="saveAttendee"
                        >Save</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-dialog>
</template>

<script>
import { ref, watch, defineProps, defineEmits, onMounted } from "vue";
import { getEventDetails, addAttendeeToEvent } from "../services/eventService";

export default {
    props: {
        eventId: Number,
        modelValue: Boolean,
    },
    setup(props, { emit }) {
        const dialog = ref(false);
        const attendeeDialog = ref(false);
        const event = ref(null);
        const newAttendee = ref({ name: "", email: "" });
        const loading = ref(false);

        // Fetch event details
        const fetchEventDetails = async () => {
            try {
                event.value = await getEventDetails(props.eventId);
            } catch (error) {
                console.error("Error fetching event details:", error);
            }
        };

        // Open add attendee dialog
        const addAttendee = () => {
            attendeeDialog.value = true;
        };

        // Save attendee to event
        const saveAttendee = async () => {
            if (!newAttendee.value.name || !newAttendee.value.email) return;

            loading.value = true;
            try {
                await addAttendeeToEvent(props.eventId, newAttendee.value);
                event.value.attendees.push({ ...newAttendee.value }); // Update UI immediately
                attendeeDialog.value = false;
                newAttendee.value = { name: "", email: "" };
            } catch (error) {
                console.error("Error adding attendee:", error);
            } finally {
                loading.value = false;
            }
        };

        // Close dialogs
        const closeDialog = () => {
            dialog.value = false;
            emit("close");
        };

        const closeAttendeeDialog = () => {
            attendeeDialog.value = false;
        };

        // Watch for dialog open and fetch event details
        watch(
            () => props.modelValue,
            (val) => {
                dialog.value = val;
                if (val && props.eventId) fetchEventDetails();
            }
        );

        return {
            dialog,
            attendeeDialog,
            event,
            newAttendee,
            loading,
            addAttendee,
            saveAttendee,
            closeDialog,
            closeAttendeeDialog,
        };
    },
};
</script>
