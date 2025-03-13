<template>
    <v-card class="pa-4">
        <v-row>
            <!-- Organizer Filter -->
            <v-col cols="12" md="4">
                <v-select
                    v-model="selectedOrganizers"
                    :items="organizers"
                    label="Organizer Filter"
                    multiple
                    @update:modelValue="emitFilters"
                >
                </v-select>
            </v-col>

            <!-- Date Filter -->
            <v-col cols="12" md="4">
                <v-menu v-model="datePicker" :close-on-content-click="false">
                    <template v-slot:activator="{ props }">
                        <v-text-field
                            v-bind="props"
                            v-model="selectedDate"
                            label="Date Filter"
                            readonly
                        ></v-text-field>
                    </template>
                    <v-date-picker v-model="selectedDate" @input="emitFilters">
                    </v-date-picker>
                </v-menu>
            </v-col>

            <!-- Search By Name -->
            <v-col cols="12" md="4">
                <v-text-field
                    v-model="searchQuery"
                    label="Search events by Name"
                    clearable
                    @input="emitFilters"
                >
                </v-text-field>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { getOrganizers } from "../services/eventService";
import { format } from "date-fns"; // Date formatting

export default {
    setup(_, { emit }) {
        const selectedOrganizers = ref([]);
        const selectedDate = ref(null);
        const searchQuery = ref("");
        const datePicker = ref(false);
        const organizers = ref([]);

        // Fetch organizers from API
        const fetchOrganizers = async () => {
            try {
                organizers.value = await getOrganizers();
            } catch (error) {
                console.error("Error fetching organizers:", error);
                organizers.value = []; // Ensure it never stays undefined
            }
        };

        // Format the date before emitting
        const formattedDate = computed(() =>
            selectedDate.value
                ? format(new Date(selectedDate.value), "yyyy-MM-dd")
                : null
        );

        // Emit filter changes
        const emitFilters = () => {
            emit("filter-updated", {
                organizers: selectedOrganizers.value,
                date: formattedDate.value,
                query: searchQuery.value,
            });
        };

        onMounted(fetchOrganizers);

        return {
            selectedOrganizers,
            selectedDate,
            formattedDate,
            searchQuery,
            datePicker,
            organizers,
            emitFilters,
        };
    },
};
</script>
