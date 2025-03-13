import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import EventListView from "../components/EventList.vue"; // List all events
import EventDetailView from "../components/EventDetails.vue"; // View single event details
import EventCreateView from "../components/EventCreate.vue"; // Create an event
//import NotFoundView from "../components/NotFoundView.vue"; // 404 Page

const routes = [
    { path: "/", component: HomeView },
    { path: "/events", component: EventListView }, // List events
    { path: "/events/:id", component: EventDetailView, props: true }, // View event details
    { path: "/events/create", component: EventCreateView }, // Create new event
    //{ path: "/:pathMatch(.*)*", component: NotFoundView }, // Catch-all 404 route
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
