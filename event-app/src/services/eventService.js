import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    withCredentials: false, // Changed to false since credentials are causing issues
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
    auth: {
        username: "vivek", // Replace with actual credentials
        password: "Vivek@2709",
    },
});

// If using token auth, add this:
// Check if token exists in localStorage
const token = localStorage.getItem("auth_token");
if (token) {
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

// Fetch all events with optional filters
export const getEvents = async (filters = {}) => {
    try {
        const response = await axios.get(`${API_URL}/events/`, {
            params: filters,
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching events:", error);
        throw error;
    }
};

// Get a single event by ID
export const getEventById = async (eventId) => {
    try {
        const response = await axios.get(`${API_URL}/events/${eventId}/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching event details:", error);
        throw error;
    }
};

// Create a new event
export const createEvent = async (eventData) => {
    console.log("Sending Event Data:", eventData);
    try {
        const response = await apiClient.post(`/events/`, eventData);
        console.log("Event Created Successfully:", response.data); // Debugging Log
        return response.data;
    } catch (error) {
        console.error("Error creating event:", error);
        console.error(
            "Error creating event:",
            error.response ? error.response.data : error
        );
        throw error;
    }
};

export const deleteEvent = async (eventId) => {
    try {
        await apiClient.delete(`/events/${eventId}/`);
        console.log("Event Deleted Successfully:", eventId);
    } catch (error) {
        console.error("Error deleting event:", error);
        throw error;
    }
};

export const updateEvent = async (eventId, updatedData) => {
    try {
        const response = await apiClient.patch(
            `/events/${eventId}/`,
            updatedData
        );
        return response.data;
    } catch (error) {
        console.error(
            "❌ Error updating event:",
            error.response?.data || error
        );
        throw error;
    }
};

export const addAttendeeToEvent = async (eventId, attendeeData) => {
    try {
        console.log("🔹 Sending Attendee Data:", attendeeData);
        const response = await apiClient.post(`/attendees/`, attendeeData);
        console.log("✅ Attendee added successfully:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error adding attendee:", error);
        throw error;
    }
};

// Delete an event

export const getOrganizers = async () => {
    try {
        const response = await axios.get(`${API_URL}/users/`);
        return response.data; // Assuming API returns an array of organizers
    } catch (error) {
        console.error("Failed to fetch organizers:", error);
        return [];
    }
};

export const getEventDetails = async (eventId) => {
    try {
        const response = await axios.get(`${API_URL}/events/${eventId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching event details:", error);
        throw error;
    }
};
