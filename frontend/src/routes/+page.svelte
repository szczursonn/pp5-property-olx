<script lang="ts">
    import { goto } from "$app/navigation";
    import { BASE_URL, getRandomOffers } from "$lib/api";
    import OfferBrowserFilterForm from "$lib/components/OfferBrowserFilterForm.svelte";
    import { SITE_TITLE } from "$lib/constants";
    import { getLocationString } from "$lib/getLocationString";
    import type { Offer } from "$lib/types";
    import { onMount } from "svelte";
    import type { PageData } from "./$types";
    
    const handleSubmit = (filter: URLSearchParams) => {
        goto(`/offers?${filter.toString()}`)
    }

    onMount(async () => {
        offers = await getRandomOffers()
    })

    let offers: Offer[]|undefined

    export let data: PageData
</script>

<svelte:head>
    <title>{SITE_TITLE}</title>
</svelte:head>

<style lang="scss">
    .search-container {
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: whitesmoke;
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
        .bottom-spacer {
            height: 100px;
        }
    }
    .suggested-container {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
    .offers {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        margin-bottom: 20px;
    }
    @media (max-width: 1000px) {
        .offers {
            grid-template-columns: 1fr 1fr;
        }
    }
    @media (max-width: 650px) {
        .offers {
            grid-template-columns: 1fr;
        }
    }
    .offer {
        height: 150px;
        padding: 10px;
        margin-top: 10px;
        padding-bottom: 110px;
        margin-bottom: 5px;
        margin-left: auto;
        margin-right: auto;
        background-color: white;
        box-shadow: 0px 0px 10px rgba(128, 128, 128, 0.5);
        transition: background-color 250ms;
        &:hover {
            background-color:antiquewhite;
        }
    }
    .offer-photo {
        width: 300px;
        height: 200px;
        object-fit: cover;
    }
    .offer-price {
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 0px;
        font-weight: bold;
        font-size: large;
    }
    .offer-info-lower {
        font-size: small;
        opacity: 80%;
        margin-top: 0px;
        margin-bottom: 5px;
    }
</style>

<div class="search-container" style="background-image: url(/assets/bg-slideshow-{data.imgId}.jpg);">
    <h1>{SITE_TITLE}</h1>
    <p>find a cool house maybe idk</p>
    <OfferBrowserFilterForm onSubmit={handleSubmit} />
    <div class="bottom-spacer"></div>
</div>

<div class="suggested-container">
    <h2>Check out these offers</h2>
    {#if offers}
        <div class="offers">
        {#each offers as offer}
            <a class="offer" href={`/offers/${offer.id}`}>
                <img class="offer-photo" src={offer.photos.length > 0 ? BASE_URL+offer.photos[0].photo : "/assets/no-photo.jpg"} alt="">
                <div>
                    <div class="offer-details">
                        <p class="offer-price">{offer.price ? `${offer.price} zł` : 'Ask for price'}</p>
                    </div>
                    <p class="offer-info-lower">{getLocationString(offer)}</p>
                </div>
            </a>
        {/each}
        </div>
    {:else}
        loading...
    {/if}
</div>