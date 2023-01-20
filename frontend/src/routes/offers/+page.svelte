<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import OfferBrowserFilterForm from "$lib/components/OfferBrowserFilterForm.svelte";
    import { OFFER_CATEGORIES, OFFER_TYPES, SITE_TITLE } from "$lib/constants";
    import type { PageData } from "./$types";
    import OfferList from "$lib/components/OfferList.svelte";

    let criteria: string[] = []

    const handleSubmit = (filter: URLSearchParams)=>{
        goto(`/offers?${filter.toString()}`)
    }

    page.subscribe((_page) => {
        let s = _page.data.params as URLSearchParams
        // undefined when preloading
        if (s===undefined) s = new URLSearchParams(location.search)
        criteria = []
        if (s.has('category')) {
            criteria.push(`Category: ${OFFER_CATEGORIES.find(cat=>cat.value.toString()===s.get('category'))!.label}`)
        }
        if (s.has('type')) {
            criteria.push(`Type: ${OFFER_TYPES.find(type=>type.value.toString()===s.get('type'))!.label}`)
        }
        if (s.has('city')) {
            criteria.push(`City: ${s.get('city')}`)
            if (s.has('proximity')) {
                criteria.push(`Proximity: ${s.get('proximity')} km`)
            }
        }
        if (s.has('price_min')) {
            criteria.push(`Price minimum: ${Number(s.get('price_min')).toFixed(0).replace('.',',')} zł`)
        }
        if (s.has('price_max')) {
            criteria.push(`Price maximum: ${Number(s.get('price_max')).toFixed(0).replace('.',',')} zł`)
        }
        if (s.has('area_min')) {
            criteria.push(`Surface area minimum: ${Number(s.get('area_min')).toFixed(2).replace('.',',')} m²`)
        }
        if (s.has('area_max')) {
            criteria.push(`Surface area maximum: ${Number(s.get('area_max')).toFixed(2).replace('.',',')} m²`)
        }
    })
    
    export let data: PageData

</script>

<svelte:head>
    <title>{data.offers.length} offers | {SITE_TITLE}</title>
</svelte:head>

<style lang="scss">
    .master-container {
        display: flex;
        align-items: center;
        flex-direction: column;
    }
    .content-container {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
</style>

<div class="master-container">
    <div class="content-container">
        <OfferBrowserFilterForm onSubmit={handleSubmit} />
        <div>
            <p>Found {data.offers.length} offers matching following criteria:</p>
            <ul>
                {#each criteria as c}
                    <li>{c}</li>
                {/each}
            </ul>
        </div>
        <OfferList offers={data.offers}></OfferList>
    </div>
</div>