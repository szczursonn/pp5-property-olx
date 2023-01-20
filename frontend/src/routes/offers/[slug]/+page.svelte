<script lang="ts">
    import { NO_IMAGE_PHOTO, SITE_TITLE } from "$lib/constants";
    import type { PageData } from "./$types";
    import { getLocationString } from "$lib/getLocationString";
    import { onDestroy } from "svelte";
    import { userStore } from "$lib/stores/user";
    import Map from "$lib/components/Map.svelte";
    import { changeOfferStatus } from "$lib/api";
    import { errorStore } from "$lib/stores/error";
    import { invalidate } from "$app/navigation";

    export let data: PageData

    let photos = (data.offer && data.offer.photos.length > 0) ? data.offer.photos : [NO_IMAGE_PHOTO]
    let selectedPhotoIndex = 0

    let isOwnedByCurrentUser = false
    onDestroy(userStore.subscribe((store)=>isOwnedByCurrentUser=data.offer?.authorId === store.user?.id))

    let isDeactivationModalOpened = false
    const openDeactivationModal = () => {
        isDeactivationModalOpened = true
    }
    const closeDeactivationModal = () => {
        isDeactivationModalOpened = false
    }

    let isChangingStatus = false
    const handleActivationButtonClick = async () => {
        isChangingStatus = true
        try {
            await changeOfferStatus(data.offer?.id!, 0)
            await invalidate(()=>true)
        } catch (err) {
            console.error(err)
            $errorStore.addError('Failed to activate offer. Check console for details.')
        }
        isChangingStatus = false
    }

    const handleDeactivateClick = async () => {
        closeDeactivationModal()
        isChangingStatus = true
        try {
            await changeOfferStatus(data.offer?.id!, 1)
            await invalidate(()=>true)
        } catch (err) {
            console.error(err)
            $errorStore.addError('Failed to deactivate offer. Check console for details.')
        }
        isChangingStatus = false
    }

</script>

<style lang="scss">
    .master-container {
        display: flex;
        align-items: center;
        flex-direction: column;
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .inner-container {
        max-width: 1024px;
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
        width: 1024px;
        @media (max-width: 1024px) {
            width: auto;
        }
        .photo {
            img {
                width: 100%;
                height: 60vh;
                object-fit: cover;
            }
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
            margin-right: 5px;
        }
    }
    .title-and-price {
        display: flex;
        justify-content: space-between;
    }
    .description {
        word-break: break-all;
    }
    .contact-info {
        display: flex;
        .email-link {
            transition: color 200ms;
            &:hover {
                color: var(--cta);
            }
        } 
    }
    .contact-icon {
        height: 25px;
        margin-right: 8px;
    }
    .author-info-container {
        display: flex;
        align-items: center;
        img {
            object-fit: cover;
            height: 80px;
            width: 80px;
            border-radius: 50%;
        }
        a {
            margin-left: 10px;
            transition: color 200ms;
            &:hover {
                color: var(--cta);
            }
        }
    }
    .activation-btn {
        color: whitesmoke;
        background-color: var(--cta);
        padding: 10px 20px;
        border-width: 0px;
        border-radius: 5px;
        font-size: medium;
        cursor: pointer;
        transition: filter 200ms;
        &:hover {
            filter: brightness(120%);
        }
    }
    .activation-info-container {
        background-color: rgba(255, 0, 0, 0.1);
        border-color: red;
        border-style: solid;
        border-width: 4px;
        border-radius: 5px;
        padding: 8px;
        .header {
            color: red;
            text-transform: uppercase;
        }
        &.active {
            background-color: rgb(0, 210, 0, 0.1);
            border-color: rgb(0, 210, 0);
            .header {
                color: rgb(0, 210, 0);
            }
        }
    }
    .deactivation-modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0,0,0, 0.4);
        &.show {
            display: block;
        }
        .content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 30%;
        }
        button {
            @extend .activation-btn;
        }
    }
</style>

<svelte:head>
    <title>{data.offer?.title ?? '404'} | {SITE_TITLE}</title>
</svelte:head>

<div class="master-container">
    <div class="inner-container">
        {#if data.offer && data.author}
            <div>
                <a class="back-button" href={globalThis?.document?.referrer} on:click|preventDefault={()=>window.history.back()}>
                    <img src="/assets/arrow.svg" alt="Back arrow icon">
                    Back
                </a>
            </div>
            <div class="gallery-container">
                <div class="photo">
                    <div class="numbertext">{selectedPhotoIndex+1} / {photos.length}</div>
                    <img src={photos[selectedPhotoIndex].url} alt='Offer photo {photos[selectedPhotoIndex].id}'>
                </div>
                {#if selectedPhotoIndex > 0}
                    <p class="prev" on:click={()=>selectedPhotoIndex--} on:keypress={()=>selectedPhotoIndex--}>❮</p>
                {/if}
                {#if selectedPhotoIndex < photos.length-1}
                    <p class="next" on:click={()=>selectedPhotoIndex++} on:keypress={()=>selectedPhotoIndex++}>❯</p>
                {/if}
            </div>
            {#if isOwnedByCurrentUser || data.offer.status === 1}
                <div class="activation-info-container" class:active={data.offer.status === 0}>
                    <h3 class="header">Offer is {data.offer.status === 0 ? 'active' : 'inactive'}</h3>
                    {#if data.offer.status === 0}
                    <p>Offer will expire on {data.offer.activeUntil.toLocaleString()}</p>
                    {:else}
                    <p>Offer has been inactive since {data.offer.activeUntil.toLocaleString()}</p>
                    <p>While the offer is inactive it will not show up in search results and on {isOwnedByCurrentUser ? 'your' : `${data.author.username}'s'`} profile.</p>
                    {/if}
                    {#if isOwnedByCurrentUser}
                    <button class="activation-btn" on:click={data.offer.status === 0 ? openDeactivationModal : handleActivationButtonClick} disabled={isChangingStatus}>
                        {data.offer.status === 0 ? 'Deactivate offer' : 'Reactivate offer'}
                    </button>
                    {/if}
                </div>
            {/if}
            <div class="title-and-price">
                <h3>{data.offer.title}</h3>
                <h3>{data.offer.price ? `${data.offer.price} zł` : 'Ask for price'}</h3>
            </div>
            <p class="category-and-type">
                {data.offer.categoryString} • {data.offer.typeString}{data.offer.squareMeters ? ` • ${data.offer.squareMeters} m²` : ''}
            </p>
            <h4 class="location-string"><img src="/assets/location-pin.svg" alt="">{getLocationString(data.offer)}</h4>
            <h3>Description</h3>
            <p class="description">{data.offer.description || 'The author did not provide any description.'}</p>
            <h3>Author</h3>
            <div class="author-info-container">
                <img src={data.author.avatar ?? NO_IMAGE_PHOTO.url} alt={`${data.author.username}'s avatar'`}>
                <a href={`/users/${data.author.id}`}>{data.author.username}</a>
            </div>
            <h4>Contact info</h4>
            <p class="contact-info">
                <img class="contact-icon" src="/assets/mail-icon.svg" alt="Email">
                <a class="email-link" href={`mailto:${data.author.email}`}>{data.author.email}</a>
            </p>
            <p class="contact-info">
                <img class="contact-icon" src="/assets/phone-icon.svg" alt="Phone number">
                {data.author.phoneNumber ?? 'Not provided'}
            </p>
            <h3>Map</h3>
            <Map coords={[data.offer.location.lat, data.offer.location.lng]} />
        {:else}
            <h2>404</h2>
        {/if}
        <div class="deactivation-modal" class:show={isDeactivationModalOpened}>
            <div class="content">
                <p>Are you sure? Deactivating the offer will cause it to not show on your profile and in search results.</p>
                <button on:click={handleDeactivateClick}>Yes</button>
                <button on:click={closeDeactivationModal}>Cancel</button>
            </div>
        </div>
    </div>
</div>