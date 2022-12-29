<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import OfferBrowserFilterForm from "$lib/components/OfferBrowserFilterForm.svelte";
    import { OFFER_CATEGORIES, OFFER_TYPES, SITE_TITLE } from "$lib/constants";
    import type { PageData } from "./$types";
    import { BASE_URL } from '$lib/api'

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
    .offers-container-container {
        background-color: whitesmoke;
        width: 100%;
    }
    .offers-container {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
    .offer {
        display: flex;
        align-items: center;
        height: 150px;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: white;
        box-shadow: 0px 0px 3px rgba(128, 128, 128, 0.25);
    }
    .offer-photo {
        width: 250px;
        height: 150px;
        object-fit: cover;
    }
    .offer-info {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        width: 75%;
        margin-left: 10px;
    }
    .offer-title {
        margin-top: 5px;
        font-weight: bold;
        font-size: medium;
    }
    .offer-price {
        display: inline-block;
        margin-top: 5px;
        font-weight: bold;
        font-size: large;
    }
    .offer-area {
        display: inline-block;
        margin-left: 10px;
        margin-top: 5px;
    }
    .offer-area-price-ratio {
        @extend .offer-area;
    }
    .offer-info-lower {
        font-size: small;
        opacity: 80%;
        margin-bottom: 5px;
    }
    @media (max-width: 600px) {
        .offer {
            flex-direction: column;
            padding-bottom: 100px;
        }
        .offer-title {
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .offer-price {
            margin-top: 0;
        }
        .offer-photo {
            width: 100%;
        }
        .offer-info {
            width: 100%;
        }
        .offer-info-lower {
            font-size: small;
            margin: 0;
        }
    }
</style>

<div class="master-container">
    <OfferBrowserFilterForm onSubmit={handleSubmit} />
    <div>
        <p>Found {data.offers.length} offers matching following criteria:</p>
        <ul>
            {#each criteria as c}
                <li>{c}</li>
            {/each}
        </ul>
    </div>
    <div class="offers-container-container">
        <div class="offers-container">
            {#each data.offers as offer}
            <a href={`/offers/${offer.id}`}>
                <div class="offer">
                    <img class="offer-photo" src={offer.photos.length > 0 ? BASE_URL+offer.photos[0].photo : "/assets/no-photo.jpg"} alt="">
                    <div class="offer-info">
                        <div>
                            <p class="offer-title">{offer.title}</p>
                            <div class="offer-details">
                                <p class="offer-price">{offer.price ? `${offer.price} zł` : 'Ask for price'}</p>
                                {#if offer.price && offer.squareMeters}
                                    <p class="offer-area-price-ratio">{(offer.price/offer.squareMeters).toFixed(2).replace('.',',')} zł/m²</p>
                                {/if}
                                {#if offer.squareMeters}
                                    <p class="offer-area">{offer.squareMeters.toFixed(2).replace('.',',')} m²</p>
                                {/if}
                            </div>
                        </div>
                        <p class="offer-info-lower">{offer.locationCityName} - Added {offer.createdAt.toLocaleDateString()}</p>
                    </div>
                </div>
            </a>
            {/each}
        </div>
    </div>
</div>