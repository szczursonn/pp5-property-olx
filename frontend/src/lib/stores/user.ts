import type { User } from "$lib/types";
import { writable } from "svelte/store";

type UserStoreData = {
    user: User|null,
    loading: boolean
}

export const userStore = writable<UserStoreData>({
    user: null,
    loading: false
})