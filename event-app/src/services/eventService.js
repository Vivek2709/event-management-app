import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

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
    try {
        const response = await axios.post(`${API_URL}/events/`, eventData);
        return response.data;
    } catch (error) {
        console.error("Error creating event:", error);
        throw error;
    }
};

// Update an event
export const updateEvent = async (eventId, updatedData) => {
    try {
        const response = await axios.patch(
            `${API_URL}/events/${eventId}/`,
            updatedData
        );
        return response.data;
    } catch (error) {
        console.error("Error updating event:", error);
        return [];
    }
};

// Delete an event
export const deleteEvent = async (eventId) => {
    try {
        await axios.delete(`${API_URL}/events/${eventId}/`);
    } catch (error) {
        console.error("Error deleting event:", error);
        throw error;
    }
};

export const getOrganizers = async () => {
    try {
        const response = await axios.get(`${API_URL}/users/`);
        return response.data; // Assuming API returns an array of organizers
    } catch (error) {
        console.error("Failed to fetch organizers:", error);
        return [];
    }
};

export const addAttendeeToEvent = async (eventId, attendeeData) => {
    try {
        const response = await axios.post(
            `${API_URL}/events/${eventId}/attendees`,
            attendeeData
        );
        return response.data;
    } catch (error) {
        console.error("Error adding attendee:", error);
        throw error;
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
