import { writable } from "svelte/store";

type ErrorStoreData = {
    errors: string[],
    clearErrors: ()=>void,
    addError: (error: string)=>void
}

export const errorStore = writable<ErrorStoreData>({
    errors: [],
    clearErrors: () => {
        errorStore.update((store)=>{
            return {...store, errors: []}
        })
    },
    addError: (error) => {
        errorStore.update((store)=>{
            return {...store, errors: [...store.errors, error]}
        })
    }
})