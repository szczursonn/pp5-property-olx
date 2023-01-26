<script lang="ts">
    import { goto } from '$app/navigation'
    import { getRandomOffers } from '$lib/api'
    import OfferBrowserFilterForm from '$lib/components/OfferBrowserFilterForm.svelte'
    import OfferGrid from '$lib/components/OfferGrid.svelte'
    import { SITE_TITLE } from '$lib/constants'
    import type { Offer } from '$lib/types'
    import { onMount } from 'svelte'
    import type { PageData } from './$types'

    const handleSubmit = (filter: URLSearchParams) => {
        goto(`/offers?${filter.toString()}`)
    }

    onMount(async () => {
        offers = await getRandomOffers()
    })

    let offers: Offer[] | undefined

    export let data: PageData
</script>

<svelte:head>
    <title>{SITE_TITLE}</title>
</svelte:head>

<div class="search-container" style="background-image: url(/assets/bg-slideshow-{data.backgroundImageId}.jpg);">
    <h1>{SITE_TITLE}</h1>
    <p>find a cool house maybe idk</p>
    <OfferBrowserFilterForm onSubmit={handleSubmit} />
</div>

{#if offers}
    <div class="suggested-container">
        <h2>Check out these offers</h2>
        <OfferGrid {offers} />
    </div>
{/if}

<style lang="scss">
    .search-container {
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: whitesmoke;
        padding-bottom: 100px;
        h1 {
            margin-top: 50px;
            padding: 6px 12px;
            text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
            font-size: 3rem;
        }
        p {
            margin-bottom: 50px;
            text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
            font-size: 1.5rem;
        }
    }
    .suggested-container {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
