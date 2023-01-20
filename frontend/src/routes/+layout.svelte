<script lang="ts">
    import { fetchUser } from "$lib/api";
    import ErrorAlertModal from "$lib/components/ErrorAlertModal.svelte";
    import { errorStore } from "$lib/stores/error";
    import { userStore } from "$lib/stores/user";
    import { onMount } from "svelte";
    import Footer from "../lib/components/Footer.svelte";
    import Navbar from "../lib/components/Navbar.svelte";

    onMount(async ()=>{
        userStore.update((currentData)=>{
            return {...currentData, loading: true}
        })
        try {
            const user = await fetchUser('me')
            userStore.update((currentData)=>{
                return {...currentData, user}
            })
        } catch (err) {
            console.error(err)
            if (err instanceof TypeError) {
                $errorStore.addError('Failed to connect to the backend.')
            } else {
                $errorStore.addError('There was an error authenticating the user. Check console for details.')
            }
        }
        userStore.update((currentData)=>{
            return {...currentData, loading: false}
        })
    })
</script>

<style style="scss">
    :root {
        --cta: #00B54B;
        --navbar-text-color: whitesmoke;
        --navbar-bg-color: #464b53;
    }
    :global(body) {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }
    :global(a) {
        text-decoration: inherit;
        color: inherit;
    }
    :global(a:visited) {
        color: inherit;
    }
    main {
        height: auto;
    }
</style>

<Navbar />
<main>
    <slot />
</main>
<Footer />
<ErrorAlertModal />