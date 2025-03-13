<template>
    <v-container>
        <h2 class="mb-4">Event Management System</h2>

        <!-- Filters -->
        <v-row class="mb-4">
            <v-col cols="12" sm="5">
                <CommonInput
                    label="Organizer Filter"
                    v-model="filters.organizer"
                    @update:modelValue="fetchEvents"
                />
            </v-col>
            <v-col cols="12" sm="5">
                <CommonInput
                    label="Date Filter"
                    type="date"
                    v-model="filters.date"
                    @update:modelValue="fetchEvents"
                />
            </v-col>
            <v-col cols="12" sm="2" class="d-flex align-center justify-end">
                <CommonButton
                    text="Add Event"
                    color="primary"
                    @click="openCreateForm"
                />
            </v-col>
        </v-row>

        <!-- Search Bar -->
        <v-text-field
            v-model="searchQuery"
            label="Search events by name"
            outlined
            dense
            class="mb-4"
            @update:modelValue="fetchEvents"
        />

        <!-- Event List -->
        <EventList
            :events="events"
            @edit="editEvent"
            @delete="confirmDelete"
            @view="viewEvent"
        />

        <!-- Create/Edit Event Dialog -->
        <CommonDialog
            v-model="showForm"
            :title="selectedEvent ? 'Edit Event' : 'Create Event'"
        >
            <EventForm
                :event="selectedEvent"
                @close="closeEventForm"
                @event-updated="fetchEvents"
            />
        </CommonDialog>

        <!-- Event Details Dialog -->
        <CommonDialog v-model="showDetails" title="Event Details">
            <EventDetails
                :eventId="selectedEventId"
                @close="showDetails = false"
            />
        </CommonDialog>

        <!-- Delete Confirmation Dialog -->
        <CommonDialog v-model="showDelete" title="Confirm Deletion">
            <DeleteEvent
                :eventId="deleteEventId"
                @close="closeDeleteDialog"
                @event-deleted="fetchEvents"
            />
        </CommonDialog>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getEvents } from "../services/eventService";
import EventList from "../components/EventList.vue";
import EventForm from "../components/EventForm.vue";
import EventDetails from "../components/EventDetails.vue";
import DeleteEvent from "../components/DeleteEvent.vue";
import CommonDialog from "../components/CommonDialog.vue";
import CommonButton from "../components/CommonButton.vue";
//import CommonInput from "../components/CommonInput.vue"; // New Input Component

const events = ref([]);
const showForm = ref(false);
const showDetails = ref(false);
const showDelete = ref(false);
const selectedEvent = ref(null);
const selectedEventId = ref(null);
const deleteEventId = ref(null);
const searchQuery = ref("");
const filters = ref({ organizer: "", date: "" });

const fetchEvents = async () => {
    try {
        events.value = await getEvents({
            search: searchQuery.value,
            ...filters.value,
        });
    } catch (error) {
        console.error("Error loading events:", error);
    }
};

const viewEvent = (event) => {
    selectedEventId.value = event.id;
    showDetails.value = true;
};

const editEvent = (event) => {
    selectedEvent.value = event;
    showForm.value = true;
};

const openCreateForm = () => {
    selectedEvent.value = null;
    showForm.value = true;
};

const closeEventForm = () => {
    selectedEvent.value = null;
    showForm.value = false;
};

const confirmDelete = (id) => {
    deleteEventId.value = id;
    showDelete.value = true;
};

const closeDeleteDialog = () => {
    deleteEventId.value = null;
    showDelete.value = false;
};

onMounted(fetchEvents);
</script>

<style scoped>
h2 {
    font-weight: 500;
}
</style>
