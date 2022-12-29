<script lang="ts">
    import { OFFER_CATEGORIES, OFFER_TYPES } from "$lib/constants";
    import type { PageData } from "./$types";
    import L from 'leaflet';
    import { getLocationString } from "$lib/getLocationString";

    export let data: PageData

    

    let photos = data.offer.photos.length > 0 ? data.offer.photos : [{id: -1, photo: "/assets/no-photo.jpg"}]
    let selectedPhotoIndex = 0

    let map: L.Map | null = null

    const coords: L.LatLngExpression = [data.offer.locationLat, data.offer.locationLng]
    const createMap = (container: HTMLElement) => {
        const m = L.map(container, {preferCanvas: true}).setView(coords, 5)
        L.tileLayer(
            'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
            {
                attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
                    &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
                subdomains: 'abcd',
                maxZoom: 20,
	        }
        ).addTo(m)

        return m
    }

    const mapAction = (container: HTMLElement) => {
        map = createMap(container);
        
        const markerLayers = L.layerGroup()
        markerLayers.addLayer(
            L.marker(coords, {
                icon: L.divIcon({
                    html: `<div class="map-marker"><img src="/assets/location-pin.svg"></div>`,
                    className: 'map-marker'
                })
            })
        )
        markerLayers.addTo(map)

        return {
            destroy: () => {
                map?.remove()
                map = null
            }
        }
    }

    const resizeMap = () => {
        map?.invalidateSize()
    }

</script>

<svelte:window on:resize={resizeMap} />

<style lang="scss">
    .master-container {
        display: flex;
        align-items: center;
        flex-direction: column;
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        margin-top: 10px;
    }
    .inner-container {
        width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
    .back-button {
        width: 80px;
        display: flex;
        border-style: solid;
        border-color: black;
        border-width: 2px;
        border-radius: 5px;
        font-weight: 700;
        padding: 2px 4px;
        margin-top: 5px;
        margin-bottom: 15px;
        img {
            width: 15px;
            rotate: 45deg;
            margin-left: 10px;
            margin-right: 10px;
        }
        &:hover {
            cursor: pointer;
        }
    }
    .gallery-container {
        position: relative;
        margin: auto;
    }
    .photo {
        img {
            width: 100%;
            height: 600px;
            object-fit: cover;
        }
    }
    .prev {
        cursor: pointer;
        position: absolute;
        top: 50%;
        width: auto;
        padding: 16px;
        margin-top: -22px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.6s ease;
        border-radius: 0 3px 3px 0;
        user-select: none;
        &:hover {
            background-color: rgba(0,0,0,0.8);
        }
    }
    .next {
        @extend .prev;
        right: 0;
        border-radius: 3px 0 0 3px;
    }
    .numbertext {
        color: #f2f2f2;
        font-size: 12px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
    }
    h3 {
        margin: 5px 0px;
    }
    .category-and-type {
        margin: 5px 0px;
    }
    .location-string {
        display: flex;
        color: var(--cta);
        margin: 5px 0px;
        font-size: smaller;
        img {
            height: 20px;
        }
    }
    .title-and-price {
        display: flex;
        justify-content: space-between;
    }
    .description {
        word-break: break-all;
    }
	
	.map :global(.map-marker) {
		width:30px;
		transform:translateX(-50%) translateY(-25%);
	}
    .map {
        min-height: 600px;
    }
    .contact-info {
        display: flex;
    }
    .contact-icon {
        height: 25px;
        margin-right: 8px;
    }
</style>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
   integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
   crossorigin=""/>
<div class="master-container">
    <div class="inner-container">
        <div>
            <a class="back-button" href={globalThis?.document?.referrer} on:click|preventDefault={()=>window.history.back()}>
                <img src="/assets/arrow.svg" alt="Back arrow icon">
                Back
            </a>
        </div>
        <div class="gallery-container">
            <div class="photo">
                <div class="numbertext">{selectedPhotoIndex+1} / {photos.length}</div>
                <img src={photos[selectedPhotoIndex].photo} alt='Offer photo {photos[selectedPhotoIndex].id}'>
            </div>
            {#if selectedPhotoIndex > 0}
                <p class="prev" on:click={()=>selectedPhotoIndex--} on:keypress={()=>selectedPhotoIndex--}>❮</p>
            {/if}
            {#if selectedPhotoIndex < photos.length-1}
                <p class="next" on:click={()=>selectedPhotoIndex++} on:keypress={()=>selectedPhotoIndex++}>❯</p>
            {/if}
        </div>
        <div class="title-and-price">
            <h3>{data.offer.title}</h3>
            <h3>{data.offer.price ? `${data.offer.price} zł` : 'Ask for price'}</h3>
        </div>
        <p class="category-and-type">
            {OFFER_CATEGORIES.find(cat=>cat.value===data.offer.category)?.label} • {OFFER_TYPES.find(type=>type.value===data.offer.type)?.label}{data.offer.squareMeters ? ` • ${data.offer.squareMeters} m²` : ''}
        </p>
        <h4 class="location-string"><img src="/assets/location-pin.svg" alt="">{getLocationString(data.offer)}</h4>
        <h3>Description</h3>
        <p class="description">{data.offer.description || 'The author did not provide any description.'}</p>
        <h3>Author</h3>
        <p class="author-name">{data.author.username}</p>
        <h4>Contact info</h4>
        {#if data.author.email}
            <p class="contact-info">
                <img class="contact-icon" src="/assets/mail-icon.svg" alt="Email">
                <a href={`mailto:${data.author.email}`}>{data.author.email}</a>
            </p>
        {/if}
        {#if data.author.phoneNumber}
            <p class="contact-info">
                <img class="contact-icon" src="/assets/phone-icon.svg" alt="Phone number">
                {data.author.phoneNumber}
            </p>
        {/if}
        <h3>Map</h3>
        <div class="map" use:mapAction/>
    </div>
</div>