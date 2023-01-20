<script lang="ts">
    import { goto } from "$app/navigation";
    import { createOffer } from "$lib/api";
    import { OFFER_CATEGORIES, OFFER_TYPES, SITE_TITLE } from "$lib/constants";
    import { userStore } from "$lib/stores/user";

    let isLoading = false
    let error: string|null = null

    let title: string = ''
    let description: string = ''
    let category: number
    let type: number
    let price: number|null = null
    let area: number|null = null
    let city: string = ''
    let streetName: string = ''
    let houseNumber: string = ''
    let apartmentNumber: string = ''

    let fileInput: HTMLInputElement
    let photos: File[] = []

    const handleFileInput = () => {
        const files = fileInput.files!
        for (let file of files) {
            photos.push(file)
        }
        photos = photos
    }
    const handleFileRemove = (f: File) => {
        const i = photos.findIndex(file=>file===f)
        photos.splice(i, 1)
        photos = photos
    }

    const handleSubmit = async () => {
        isLoading = true
        try {
            const offerId = await createOffer({
                title,
                description,
                category,
                type,
                price: price === null ? undefined : price,
                squareMeters: area === null ? undefined : area,
                cityName: city,
                streetName,
                houseNumber,
                apartmentNumber,
                photos
            })
            goto(`/offers/${offerId}`)
        } catch (err) {
            error=String(err)
        }
        isLoading = false
    }
</script>

<style lang="scss">
    .inner-container {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        padding-bottom: 32px;
    }
    form {
        display: flex;
        flex-direction: column;
        padding: 20px 20px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .number-form-input {
        display: inline-flex;
        align-items: center;
        input {
            flex: 1;
        }
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
    .select-container {
        display: flex;
        select {
            flex: 1;
        }
        span {
            width: 5px;
        }
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
    h4 {
        margin-top: 0px;
        margin-bottom: 10px;
    }
    input[type=file] {
        display: none;
    }
    .file-upload-label {
        border: 1px solid black;
        display: inline-block;
        padding: 6px 12px;
        cursor: pointer;
        margin-bottom: 10px;
        max-width: 60px;
    }
    .photos-container {
        display: flex;
        flex-wrap: wrap;
        .photo-container {
            position: relative;
            .photo {
            margin: 3px;
            width: 250px;
            height: 150px;
            }
            .photo-close-btn {
                display: none;
                position: absolute;
                top: 5px;
                right: 5px;
                height: 30px;
                width: 30px;
                rotate: 45deg;
                filter: invert(0.5) sepia(1) saturate(5) hue-rotate(320deg);
                cursor: pointer;
            }
            &:hover {
                .photo-close-btn {
                    display: block;
                }
            }
        }
    }
    .login-link {
        cursor: pointer;
        transition: color 200ms;
        &:hover {
            color: var(--cta);
        }
    }
</style>

<svelte:head>
    <title>New offer | {SITE_TITLE}</title>
</svelte:head>

<div class="inner-container">
    <h2>Create an offer</h2>
    {#if $userStore.user}
    <form on:submit|preventDefault={handleSubmit}>
        <h3>Title and description</h3>
        <h4>Title is required, it is highly recommended to add a description</h4>
        <input type="text" placeholder="Title" required={true} bind:value={title}>
        <textarea placeholder="Description" bind:value={description}></textarea>
        <h3>Category</h3>
        <h4>Select category and type of your offer</h4>
        <div class="select-container">
            <select bind:value={category}>
                {#each OFFER_CATEGORIES as {label, value}}
                    <option value={value}>{label}</option>
                {/each}
            </select>
            <span></span>
            <select bind:value={type}>
                {#each OFFER_TYPES as {label, value}}
                    <option value={value}>{label}</option>
                {/each}
            </select>
        </div>
        <h3>Parameters</h3>
        <h4>Setting these will help users see your offers</h4>
        <div class="number-form-input">
            <input type="number" placeholder="Price" min={0} bind:value={price}>
            <span>zł</span>
            <input type="number" placeholder="Surface area" min={0} bind:value={area}>
            <span>m²</span>
        </div>
        <h3>Location</h3>
        <h4>City is required, other fields are recommended</h4>
        <div>
            <input type="text" placeholder="City" required={true} bind:value={city}>
            <input type="text" placeholder="Street name" bind:value={streetName}>
            <input type="text" placeholder="House number" bind:value={houseNumber}>
            <input type="text" placeholder="Apartment number" bind:value={apartmentNumber}>
        </div>
        <h3>Photos</h3>
        <h4>Attach photos here</h4>
        <label for="file-upload" class="file-upload-label">Upload</label>
        <input id="file-upload" type="file" name="Photos" accept="image/*" multiple={true} bind:this={fileInput} on:change={handleFileInput}>
        <div class="photos-container">
            {#each photos as file}
                <div class="photo-container">
                    <img class="photo" src={URL.createObjectURL(file)} alt={''}>
                    <img class="photo-close-btn" src="/assets/plus-icon.svg" alt="" on:click={()=>handleFileRemove(file)} on:keypress={()=>handleFileRemove(file)}>
                </div>
            {/each}
        </div>
        {#if error}
            <p>There was an error: </p>
            <pre>{error}</pre>
        {/if}
        <input type="submit" value="Create" disabled={isLoading || title.length === 0 || city.length === 0}>
    </form>
    {:else}
        <h3>You need to be signed in to add an offer</h3>
        <a class="login-link" href="/login">Sign in</a>
    {/if}
</div>