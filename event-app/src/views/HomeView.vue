<template>
    <v-container fluid fill-height class="pa-6">
        <!-- Header Title -->
        <v-row>
            <v-col>
                <h2 class="font-weight-bold text-primary">
                    Event Management System
                </h2>
            </v-col>
        </v-row>

        <v-row>
            <!-- Left Column (Static Text) -->
            <v-col cols="3">
                <h3 class="font-weight-bold text-secondary">Events</h3>
            </v-col>

            <!-- Right Column (Styled Card Container) -->
            <v-col cols="9">
                <v-card class="pa-5 event-container">
                    <!-- Filters & Add Event Button (Flex Aligned) -->
                    <v-row class="mb-4 align-center">
                        <!-- Organizer Filter -->
                        <v-col cols="4">
                            <v-select
                                v-model="organizerFilter"
                                :items="organizers"
                                item-title="name"
                                item-value="id"
                                label="Organizer Filter"
                                dense
                                outlined
                                class="custom-select"
                            ></v-select>
                        </v-col>

                        <!-- Date Picker (inside v-col to stay in same row) -->
                        <v-col cols="4">
                            <VueDatePicker
                                v-model="selectedDate"
                                placeholder="Select Date"
                                :enable-timepicker="false"
                                auto-apply
                                input-class-name="date-picker-input"
                                text-input
                            />
                        </v-col>

                        <!-- Add Event Button (Right aligned) -->
                        <v-col cols="4" class="text-right">
                            <v-btn
                                color="primary"
                                @click="openAddEventDialog"
                                class="custom-button"
                            >
                                + Add Event
                            </v-btn>
                        </v-col>
                    </v-row>

                    <!-- Search Bar -->
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="searchQuery"
                                label="Search Event"
                                append-icon="mdi-magnify"
                                dense
                                clearable
                                outlined
                                class="custom-select"
                                @input="applyFilters"
                            ></v-text-field>
                        </v-col>
                    </v-row>

                    <!-- Events List -->
                    <v-card outlined class="pa-4 event-list-container">
                        <h3 class="font-weight-bold mb-3 text-secondary">
                            Event List
                        </h3>
                        <v-list>
                            <v-list-item
                                v-for="event in events"
                                :key="event.id"
                                class="event-item mb-2"
                            >
                                <!-- Event Title -->
                                <div
                                    class="d-flex align-center justify-space-between w-100"
                                >
                                    <div class="event-title">
                                        {{ event.title }}
                                    </div>

                                    <!-- Action Buttons -->
                                    <div class="d-flex">
                                        <v-btn
                                            icon
                                            small
                                            class="mx-1"
                                            @click="openEditDialog(event)"
                                        >
                                            <v-icon
                                                >mdi-eye-circle-outline</v-icon
                                            >
                                        </v-btn>
                                        <v-btn
                                            icon
                                            small
                                            class="mx-1"
                                            @click="viewEventDetails(event.id)"
                                        >
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        <v-btn
                                            icon
                                            small
                                            class="mx-1"
                                            @click="confirmDelete(event.id)"
                                        >
                                            <v-icon
                                                >mdi-trash-can-outline</v-icon
                                            >
                                        </v-btn>
                                    </div>
                                </div>
                            </v-list-item>
                        </v-list>

                        <!-- Loading indicator -->
                        <div v-if="loading" class="text-center my-4">
                            <v-progress-circular
                                indeterminate
                                color="primary"
                            ></v-progress-circular>
                        </div>

                        <!-- No events message -->
                        <div
                            v-if="!loading && events.length === 0"
                            class="text-center my-4"
                        >
                            No events found
                        </div>
                    </v-card>
                </v-card>
            </v-col>
        </v-row>

        <!-- Add/Edit Event Dialog -->
        <v-dialog v-model="eventDialog" max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="text-h5">{{
                        dialogMode === "add" ? "Add New Event" : "Edit Event"
                    }}</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="eventForm.title"
                                    label="Event Title"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="eventForm.description"
                                    label="Event Description"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="eventForm.location"
                                    label="Event Location"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-select
                                    v-model="eventForm.organizer"
                                    :items="organizers"
                                    item-text="name"
                                    item-value="id"
                                    label="Organizer"
                                    return-object
                                    required
                                ></v-select>
                            </v-col>
                            <v-col cols="12">
                                <VueDatePicker
                                    v-model="eventForm.event_date"
                                    placeholder="Select Event Date"
                                    :format="formatDate"
                                    class="custom-select"
                                />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="eventDialog = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="saveEvent">
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Delete Confirmation Dialog -->
        <v-dialog v-model="deleteDialog" max-width="400">
            <v-card>
                <v-card-title class="text-h5"> Delete Event </v-card-title>
                <v-card-text>
                    Are you sure you want to delete this event? This action
                    cannot be undone.
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="deleteDialog = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        color="red darken-1"
                        text
                        @click="deleteEventConfirmed"
                    >
                        Delete
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Event Details Dialog -->
        <v-dialog v-model="detailsDialog" max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Event Details</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <h3>{{ selectedEvent.title }}</h3>
                                <p>
                                    <strong>Description:</strong>
                                    {{ selectedEvent.description }}
                                </p>
                                <p>
                                    <strong>Location:</strong>
                                    {{ selectedEvent.location }}
                                </p>
                                <p>
                                    <strong>Organizer:</strong>
                                    {{ selectedEvent.organizer }}
                                </p>
                                <p>
                                    <strong>Date:</strong>
                                    {{ selectedEvent.event_date }}
                                </p>
                            </v-col>
                            <v-col cols="12">
                                <h4>Attendees</h4>
                                <v-list>
                                    <v-list-item
                                        v-for="attendee in selectedEvent.attendees"
                                        :key="attendee.id"
                                    >
                                        {{ attendee.name }}
                                    </v-list-item>
                                </v-list>
                                <v-btn
                                    color="primary"
                                    @click="openAddAttendeeDialog"
                                >
                                    + Add Attendee
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="detailsDialog = false"
                    >
                        Close
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Add Attendee Dialog -->
        <v-dialog v-model="addAttendeeDialog" max-width="400px">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Add Attendee</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-select
                                    v-model="attendeeForm.event"
                                    :items="events"
                                    item-text="title"
                                    item-value="id"
                                    label="Select Event"
                                    required
                                ></v-select>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="attendeeForm.name"
                                    label="Attendee Name"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="attendeeForm.email"
                                    label="Attendee Email"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="attendeeForm.contact_number"
                                    label="Attendee Contact Number"
                                    required
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="addAttendeeDialog = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="saveAttendee">
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import {
    getEvents,
    getEventById,
    createEvent,
    updateEvent,
    deleteEvent as apiDeleteEvent,
    getOrganizers,
    getEventDetails,
    addAttendeeToEvent,
} from "../services/eventService";
import { ref } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
    components: {
        VueDatePicker,
    },

    data() {
        return {
            // Filters & Search
            organizerFilter: null,
            searchQuery: "",
            organizers: [],

            // Date Picker
            selectedDate: null,
            maxDate: new Date().toISOString().split("T")[0],

            // Events
            events: [],
            loading: false,

            // Event Form Dialog
            eventDialog: false,
            dialogMode: "add", // 'add' or 'edit'
            eventForm: {
                id: null,
                title: "",
                description: "",
                location: "",
                organizer: null,
                event_date: null,
            },

            // Delete Dialog
            deleteDialog: false,
            eventToDelete: null,

            // Event Details Dialog
            detailsDialog: false,
            selectedEvent: {
                id: null,
                title: "",
                description: "",
                location: "",
                organizer: "",
                event_date: "",
                attendees: [],
            },

            // Add Attendee Dialog
            addAttendeeDialog: false,
            attendeeForm: {
                event: null,
                name: "",
                email: "",
                contact_number: "",
            },
        };
    },

    computed: {
        formattedDate() {
            return this.formatDate(this.selectedDate);
        },
        formattedEventDate() {
            return this.formatDate(this.eventForm.event_date);
        },
        organizerName() {
            if (
                this.eventForm.organizer &&
                typeof this.eventForm.organizer === "object"
            ) {
                return this.eventForm.organizer.name;
            } else if (this.eventForm.organizer) {
                // Find the organizer by ID
                const org = this.organizers.find(
                    (o) => o.id === this.eventForm.organizer
                );
                return org ? org.name : "";
            }
            return "";
        },
    },

    methods: {
        confirmDelete(eventId) {
            this.eventToDelete = eventId;
            this.deleteDialog = true;
        },
        showSnackbar(message, color = "info") {
            this.$root.$emit("show-snackbar", { message, color });
        },

        formatDate(date) {
            return date ? new Date(date).toISOString().split("T")[0] : "";
        },
        async fetchEvents() {
            this.loading = true;
            try {
                const filters = this.buildFilters();
                const data = await getEvents(filters);
                this.events = data;
            } catch (error) {
                console.error("Error fetching events:", error);
                this.showSnackbar("Failed to load events", "error");
            } finally {
                this.loading = false;
            }
        },

        async fetchOrganizers() {
            try {
                const data = await getOrganizers();
                this.organizers = data.map((org) => ({
                    id: org.id, // Store only ID
                    name: org.username || org.name, // Ensure correct field
                }));
            } catch (error) {
                console.error("Error fetching organizers:", error);
                this.showSnackbar("Failed to load organizers", "error");
            }
        },

        buildFilters() {
            const filters = {};

            if (this.searchQuery) {
                filters.search = this.searchQuery;
            }

            if (this.organizerFilter) {
                // Find the organizer object based on selected ID
                const selectedOrganizer = this.organizers.find(
                    (org) => org.id === this.organizerFilter
                );

                // API expects organizer **username**, not ID
                filters.organizer = selectedOrganizer
                    ? selectedOrganizer.name
                    : "";
            }

            if (this.selectedDate) {
                // Format the date for the API
                filters.event_date =
                    this.selectedDate instanceof Date
                        ? this.selectedDate.toISOString().split("T")[0]
                        : this.selectedDate;
            }

            return filters;
        },

        applyFilters() {
            console.log("Applying filters with date:", this.selectedDate);

            const filters = {};

            if (this.searchQuery) {
                filters.search = this.searchQuery;
            }

            if (this.organizerFilter) {
                filters.organizer = this.organizerFilter; // Send only the ID, not the full object
            }

            if (this.selectedDate) {
                filters.event_date = this.selectedDate;
            }

            this.fetchEvents(filters);
            this.fetchEvents();
        },

        openAddEventDialog() {
            this.dialogMode = "add";
            this.eventForm = {
                id: null,
                title: "",
                description: "",
                location: "",
                organizer: null,
                event_date: null,
            };
            this.eventDialog = true;
        },

        async openEditDialog(event) {
            this.dialogMode = "edit";
            this.loading = true;

            try {
                const eventDetails = await getEventById(event.id);

                // Ensure organizer is stored as an object
                const selectedOrganizer = this.organizers.find(
                    (org) => org.name === eventDetails.organizer
                );

                this.eventForm = {
                    id: eventDetails.id,
                    title: eventDetails.title,
                    description: eventDetails.description,
                    location: eventDetails.location,
                    organizer: selectedOrganizer || {
                        id: eventDetails.organizer,
                        name: "Unknown",
                    }, // Ensure object format
                    event_date: eventDetails.event_date, // VueDatePicker compatible
                };

                this.eventDialog = true;
            } catch (error) {
                console.error("Error loading event details:", error);
                this.$root.$emit("show-snackbar", {
                    message: "⚠️ Failed to load event details",
                    color: "error",
                });
            } finally {
                this.loading = false;
            }
        },

        async saveEvent() {
            this.loading = true;

            try {
                // Ensure event_date is in YYYY-MM-DD format
                let formattedDate =
                    this.eventForm.event_date instanceof Date
                        ? this.eventForm.event_date.toISOString().split("T")[0]
                        : this.eventForm.event_date;

                // Check if the event date is in the past
                const today = new Date().toISOString().split("T")[0];
                if (formattedDate < today) {
                    console.warn(
                        "Event date cannot be in the past:",
                        formattedDate
                    );
                    this.$root.$emit("show-snackbar", {
                        message: "Event Date cannot be in the past",
                        color: "error",
                    });
                    return;
                }

                const payload = {
                    ...this.eventForm,
                    event_date: formattedDate,
                    organizer: this.eventForm.organizer.id,
                };

                console.log("Sending Event Data:", payload);

                if (this.dialogMode === "add") {
                    await createEvent(payload);
                    this.$root.$emit("show-snackbar", {
                        message: "Event updated successfully",
                        color: "success",
                    });
                } else {
                    await updateEvent(this.eventForm.id, payload);
                    this.$root.$emit("show-snackbar", {
                        message: "Event updated successfully",
                        color: "success",
                    });
                }

                this.fetchEvents();
                this.eventDialog = false;
            } catch (error) {
                console.error(
                    "Error saving event:",
                    error.response?.data || error
                );
                this.showSnackbar("Failed to save event", "error");
            } finally {
                this.loading = false;
            }
        },
        async deleteEventConfirmed() {
            this.loading = true;

            try {
                if (!this.eventToDelete) {
                    console.warn("No event selected for deletion");
                    this.$root.$emit("show-snackbar", {
                        message: "No event selected",
                        color: "error",
                    });
                    return;
                }

                await apiDeleteEvent(this.eventToDelete);
                this.$root.$emit("show-snackbar", {
                    message: "Event deleted successfully",
                    color: "success",
                });

                this.fetchEvents();
                this.deleteDialog = false;
                this.eventToDelete = null;
            } catch (error) {
                console.error("Error deleting event:", error);
                this.$root.$emit("show-snackbar", {
                    message: "Failed to delete event",
                    color: "error",
                });
            } finally {
                this.loading = false;
            }
        },
        async viewEventDetails(eventId) {
            try {
                const eventDetails = await getEventDetails(eventId);
                this.selectedEvent = eventDetails;
                this.detailsDialog = true;
            } catch (error) {
                console.error("Error fetching event details:", error);
                this.showSnackbar("Failed to load event details", "error");
            }
        },

        openAddAttendeeDialog() {
            this.attendeeForm = {
                name: "",
                email: "",
                contact_number: "",
            };
            this.addAttendeeDialog = true;
        },

        async saveAttendee() {
            console.log("saveAttendee() triggered");

            try {
                if (!this.selectedEvent || !this.selectedEvent.id) {
                    console.warn(" No event selected for attendee");
                    this.$root.$emit("show-snackbar", {
                        message:
                            "Please select an event before adding an attendee",
                        color: "error",
                    });
                    return;
                }

                const eventId = this.selectedEvent.id;
                console.log("📌 Event ID:", eventId);

                // Prepare attendee payload
                const attendeePayload = {
                    event: eventId,
                    name: this.attendeeForm.name,
                    email: this.attendeeForm.email,
                    contact_number: this.attendeeForm.contact_number,
                };

                console.log("Sending Attendee Data:", attendeePayload);

                // 🔹 Fetch event details from API
                console.log("Fetching event details...");
                const eventDetails = await getEventDetails(eventId);
                console.log("Full Event Details Response:", eventDetails);

                if (!eventDetails || !Array.isArray(eventDetails.attendees)) {
                    console.warn(
                        "Event details not loaded or missing attendees"
                    );
                    console.log("Response Data:", eventDetails); // Debugging
                    this.$root.$emit("show-snackbar", {
                        message: "Failed to load event attendees",
                        color: "error",
                    });
                    return;
                }

                // Check for duplicate attendee
                const isDuplicate = eventDetails.attendees.some(
                    (att) => att.email === this.attendeeForm.email
                );
                if (isDuplicate) {
                    console.warn(
                        "Duplicate email found:",
                        this.attendeeForm.email
                    );
                    this.$root.$emit("show-snackbar", {
                        message:
                            "This email is already registered for the event",
                        color: "error",
                    });
                    return;
                }

                console.log("Sending API request to add attendee...");
                await addAttendeeToEvent(eventId, attendeePayload);
                console.log("Attendee added successfully");

                this.$root.$emit("show-snackbar", {
                    message: "Attendee added successfully",
                    color: "success",
                });

                this.addAttendeeDialog = false;

                // 🔹 Refresh attendees list
                console.log("Refreshing event attendees...");
                const updatedEvent = await getEventDetails(eventId);
                this.selectedEvent.attendees = updatedEvent?.attendees || [];
                console.log(
                    "Updated attendees list:",
                    this.selectedEvent.attendees
                );
            } catch (error) {
                console.error("Error adding attendee:", error);
                this.$root.$emit("show-snackbar", {
                    message: "Failed to add attendee",
                    color: "error",
                });
            }
        },
    },

    created() {
        this.fetchOrganizers();
        this.fetchEvents();
    },

    watch: {
        organizerFilter() {
            this.applyFilters();
        },
        selectedDate() {
            console.log("Date selected:", this.selectedDate);
            this.applyFilters();
        },
        // selectedDate(newDate) {
        //     console.log("Selected Date:", newDate); // Check value in console
        //     this.fetchEvents();
        // },
    },
};
</script>

<style scoped>
.date-picker-container {
    width: 100%;
}
.date-picker-input {
    height: 40px;
    width: 100%;
    padding: 0 12px;
    border-radius: 8px;
    border: 1px solid rgba(0, 0, 0, 0.23);
}
/* Match the first UI styling */
.event-container {
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    background: #fff;
}

.text-primary {
    color: #3f51b5;
}

.text-secondary {
    color: #757575;
}

.custom-select {
    border-radius: 8px;
}

.custom-button {
    font-weight: bold;
    padding: 8px 16px;
}

.event-list-container {
    background: #f9f9f9;
    border-radius: 8px;
}

.event-item {
    background: #f0f0f0;
    border-radius: 4px;
    padding: 8px 16px !important;
}

.event-item:hover {
    background: #e3f2fd;
}

.event-title {
    font-size: 1rem;
    font-weight: 500;
}

.event-actions {
    display: flex;
    gap: 10px;
    flex-shrink: 0;
    align-items: center;
}

.v-btn {
    min-width: 36px;
    height: 36px;
}
.v-btn:hover {
    transform: scale(1.1);
    transition: 0.2s ease-in-out;
}
</style>
