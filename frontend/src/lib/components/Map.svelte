<script lang="ts">
    import L from 'leaflet'

    const defaultZoom = 6
    let map: L.Map | null = null
    export let coords: L.LatLngExpression

    const createMap = (container: HTMLElement) => {
        const m = L.map(container, { preferCanvas: true }).setView(coords, defaultZoom)
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
                    &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
            subdomains: 'abcd',
            maxZoom: 20,
        }).addTo(m)

        return m
    }

    const mapAction = (container: HTMLElement) => {
        map = createMap(container)

        const markerLayers = L.layerGroup()
        markerLayers.addLayer(
            L.marker(coords, {
                icon: L.divIcon({
                    html: `<div class="map-marker"><img src="/assets/location-pin.svg"></div>`,
                    className: 'map-marker',
                }),
            })
        )

        markerLayers.addTo(map)

        return {
            destroy: () => {
                map?.remove()
                map = null
            },
        }
    }

    const resizeMap = () => {
        map?.invalidateSize()
    }
</script>

<svelte:window on:resize={resizeMap} />

<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
    integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
    crossorigin=""
/>
<div class="map" use:mapAction />

<style lang="scss">
    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-50%) translateY(-25%);
        left: 8px;
        top: -8px;
    }
    .map {
        min-height: 600px;
        border-radius: 5px;
        box-shadow: 0px 0px 2px var(--navbar-bg-color);
    }
</style>
