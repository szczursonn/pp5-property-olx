<script lang="ts">
    import { OFFER_CATEGORIES, OFFER_TYPES } from "$lib/constants";
    import { page } from '$app/stores'

    let category: number
    let type: number
    let city: string = ''
    let proximity: number
    let priceMin: number|null = null
    let priceMax: number|null = null
    let areaMin: number|null = null
    let areaMax: number|null = null

    const PROXIMITY_OPTIONS = [0,5,10,15,25,50,75]

    const handleSubmit = () => {
        
        // validation here
        
        const searchParams = new URLSearchParams()
        searchParams.set('category', category.toString())
        searchParams.set('type', type.toString())
        if (city) searchParams.set('city', city)
        searchParams.set('proximity', proximity.toString())
        if (priceMin) searchParams.set('price_min', priceMin.toString())
        if (priceMax) searchParams.set('price_max', priceMax.toString())
        if (areaMin) searchParams.set('area_min', areaMin.toString())
        if (areaMax) searchParams.set('area_max', areaMax.toString())

        onSubmit(searchParams)
    }

    page.subscribe(_page=>{
        const params = new URLSearchParams(_page.url.search)
        const _category = params.get('category')
        const _type = params.get('type')
        const _city = params.get('city')
        const _proximity = params.get('proximity')
        const _priceMin = params.get('price_min')
        const _priceMax = params.get('price_max')
        const _areaMin = params.get('area_min')
        const _areaMax = params.get('area_max')
        category = _category ? parseInt(_category) : 0
        type = _type ? parseInt(_type) : 0
        city = _city === null ? '' : _city
        proximity = _proximity ? parseInt(_proximity) : 0
        priceMin = _priceMin ? parseInt(_priceMin) : null
        priceMax = _priceMax ? parseInt(_priceMax) : null
        areaMin = _areaMin ? parseInt(_areaMin) : null
        areaMax = _areaMax ? parseInt(_areaMax) : null
    })

    export let onSubmit: (filter: URLSearchParams)=>void
    
</script>

<style lang="scss">
    form {
        max-width: 1024px;
        background-color: white;
        padding: 20px 20px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .filter-form-input {
        display: inline-flex;
        align-items: center;
        span {
            position: relative;
            left: -24px;
            color: black;
            font-size: small;
        }
    }
    input {
        padding: 8px 12px;
        margin: 6px 0;
        box-sizing: border-box;
    }
    select {
        @extend input;
    }
    input[type=submit] {
        color: whitesmoke;
        background-color: var(--cta);
        padding: 9px 30px;
        border-width: 1px;
        border-radius: 3px;
        transition: filter 250ms;
        &:hover {
            filter: brightness(120%);
            cursor: pointer;
        }
    }
</style>

<form on:submit|preventDefault={handleSubmit}>
    <select bind:value={category}>
        {#each OFFER_CATEGORIES as {label, value}}
            <option value={value}>{label}</option>
        {/each}
    </select>
    <select bind:value={type}>
        {#each OFFER_TYPES as {label, value}}
            <option value={value}>{label}</option>
        {/each}
    </select>
    <input type="text" placeholder="City" bind:value={city}>
    <select bind:value={proximity}>
        {#each PROXIMITY_OPTIONS as value}
            <option value={value}>{value} km</option>
        {/each}
    </select>
    <div class="filter-form-input">
        <input type="number" placeholder="Price minimum" bind:value={priceMin}>
        <span>zł</span>
    </div>
    <div class="filter-form-input">
        <input type="number" placeholder="Price maximum" bind:value={priceMax}>
        <span>zł</span>
    </div>
    <div class="filter-form-input">
        <input type="number" placeholder="Surface area minimum" bind:value={areaMin}>
        <span>m²</span>
    </div>
    <div class="filter-form-input">
        <input type="number" placeholder="Surface area maximum" bind:value={areaMax}>
        <span>m²</span>
    </div>
    <input type="submit" value="Find">
</form>