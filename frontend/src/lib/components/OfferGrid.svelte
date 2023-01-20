<script lang="ts">
    import { BASE_URL } from "$lib/api";
    import { NO_IMAGE_PHOTO } from "$lib/constants";
    import { getLocationString } from "$lib/getLocationString";
    import type { Offer } from "$lib/types";

    export let offers: Offer[]

</script>

<style lang="scss">
    .offers-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        margin-bottom: 20px;
    }
    @media (max-width: 1000px) {
        .offers-container {
            grid-template-columns: 1fr 1fr;
        }
    }
    @media (max-width: 650px) {
        .offers-container {
            grid-template-columns: 1fr;
        }
    }
    .card {
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
    .photo {
        width: 300px;
        height: 200px;
        object-fit: cover;
    }
    .price {
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 0px;
        font-weight: bold;
        font-size: large;
    }
    .inactive {
        color: red;
        float: right;
    }
    .info-lower {
        font-size: small;
        opacity: 80%;
        margin-top: 0px;
        margin-bottom: 5px;
    }
</style>

<div class="offers-container">
    {#each offers as offer}
        <a class="card" href={`/offers/${offer.id}`}>
            <img class="photo" src={offer.photos.length > 0 ? offer.photos[0].url : NO_IMAGE_PHOTO.url} alt="">
            <div>
                <div>
                    <p class="price">{offer.price ? `${offer.price} zł` : 'Ask for price'}</p>
                    {#if offer.status === 1}
                        <p class="inactive">INACTIVE</p>
                    {/if}
                </div>
                <p class="info-lower">{getLocationString(offer)}</p>
            </div>
        </a>
    {/each}
</div>