<script lang="ts">
    import { NO_IMAGE_PHOTO } from '$lib/constants'
    import type { Offer } from '$lib/types'

    export let offers: Offer[]
</script>

<div class="offers-list">
    {#each offers as offer}
        <a href={`/offers/${offer.id}`}>
            <div class="card">
                <img class="card-image" src={offer.photos.length > 0 ? offer.photos[0].url : NO_IMAGE_PHOTO.url} alt="" />
                <div class="card-content">
                    <div>
                        <p class="card-header">{offer.title}</p>
                        <div>
                            <p class="price">{offer.price ? `${offer.price} zł` : 'Ask for price'}</p>
                            {#if offer.price && offer.squareMeters}
                                <p class="area-price-ratio">{(offer.price / offer.squareMeters).toFixed(2).replace('.', ',')} zł/m²</p>
                            {/if}
                            {#if offer.squareMeters}
                                <p class="area">{offer.squareMeters.toFixed(2).replace('.', ',')} m²</p>
                            {/if}
                        </div>
                    </div>
                    <p class="card-footer">{offer.location.city} - Added {offer.createdAt.toLocaleDateString()}</p>
                </div>
            </div>
        </a>
    {/each}
</div>

<style lang="scss">
    .offers-list {
        background-color: whitesmoke;
        width: 100%;
    }
    .card {
        display: flex;
        align-items: center;
        height: 150px;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: white;
        box-shadow: 0px 0px 3px rgba(128, 128, 128, 0.25);
    }
    .card-header {
        margin-top: 5px;
        font-weight: bold;
        font-size: medium;
    }
    .card-image {
        width: 250px;
        height: 150px;
        object-fit: cover;
        flex-shrink: 0;
    }
    .card-content {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        width: 75%;
        margin-left: 10px;
    }
    .price {
        display: inline-block;
        margin-top: 5px;
        font-weight: bold;
        font-size: large;
    }
    .area {
        display: inline-block;
        margin-left: 10px;
        margin-top: 5px;
    }
    .area-price-ratio {
        @extend .area;
    }
    .card-footer {
        font-size: small;
        opacity: 80%;
        margin-bottom: 5px;
    }
    @media (max-width: 600px) {
        .card {
            flex-direction: column;
            padding-bottom: 100px;
        }
        .card-header {
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .card-image {
            width: 100%;
        }
        .card-content {
            width: 100%;
        }
        .price {
            margin-top: 0;
        }
        .card-footer {
            font-size: small;
            margin: 0;
        }
    }
</style>
