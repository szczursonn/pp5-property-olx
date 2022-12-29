<script lang="ts">
    import { fetchUser } from "$lib/api";
    import { userStore } from "$lib/stores/user";
    import { onMount } from "svelte";
    import Footer from "../lib/components/Footer.svelte";
    import Navbar from "../lib/components/Navbar.svelte";

    onMount(async ()=>{
        userStore.update((currentData)=>{
            return {...currentData, loading: true}
        })
        const user = await fetchUser('me')
        userStore.update((currentData)=>{
            return {...currentData, user, loading: false}
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