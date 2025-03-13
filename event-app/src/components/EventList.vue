<template>
    <v-container>
        <h2>Events</h2>
        <EventFilters @filter-updated="fetchEvents" />

        <v-data-table :headers="headers" :items="events" item-value="id">
            <template v-slot:item="{ item }">
                <tr>
                    <td>{{ item.title }}</td>
                    <td>{{ item.date }}</td>
                    <td>{{ item.organizer }}</td>
                    <td>
                        <v-btn @click="viewEvent(item.id)" color="info" icon>
                            <v-icon>mdi-eye</v-icon>
                        </v-btn>
                        <v-btn @click="editEvent(item)" color="warning" icon>
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                        <v-btn
                            @click="confirmDelete(item.id)"
                            color="error"
                            icon
                        >
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                    </td>
                </tr>
            </template>
        </v-data-table>

        <!-- Dialogs -->
        <EventForm
            v-if="showForm"
            :event="selectedEvent"
            @close="showForm = false"
            @event-updated="fetchEvents"
        />
        <DeleteEvent
            v-if="showDelete"
            :event-id="deleteEventId"
            @close="showDelete = false"
            @event-deleted="fetchEvents"
        />
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getEvents, deleteEvent } from "../services/eventService";
import EventFilters from "../components/EventFilters.vue";
import EventForm from "../components/EventForm.vue";
import DeleteEvent from "../components/DeleteEvent.vue";

const events = ref([]);
const showForm = ref(false);
const showDelete = ref(false);
const selectedEvent = ref(null);
const deleteEventId = ref(null);

const headers = [
    { title: "Title", key: "title" },
    { title: "Date", key: "date" },
    { title: "Organizer", key: "organizer" },
    { title: "Actions", key: "actions", sortable: false },
];

const fetchEvents = async (filters = {}) => {
    try {
        const data = await getEvents(filters);
        events.value = data || []; // Ensure empty array if API returns null
    } catch (error) {
        console.error("Error loading events:", error);
    }
};

const viewEvent = (id) => {
    selectedEvent.value = null; // Reset before updating
    selectedEvent.value = events.value.find((event) => event.id === id);
    showForm.value = true;
};

const editEvent = (event) => {
    selectedEvent.value = null;
    selectedEvent.value = event;
    showForm.value = true;
};

const confirmDelete = async (id) => {
    if (!confirm("Are you sure?")) return;

    try {
        await deleteEvent(id);
        await fetchEvents(); // Ensure refresh
    } catch (error) {
        console.error("Failed to delete event:", error);
    }
};

onMounted(fetchEvents);
</script>
