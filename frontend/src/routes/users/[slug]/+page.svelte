<script lang="ts">
    import { changeAvatar, changeUsername } from "$lib/api";
    import OfferGrid from "$lib/components/OfferGrid.svelte";
    import { NO_IMAGE_PHOTO, SITE_TITLE } from "$lib/constants";
    import { errorStore } from "$lib/stores/error";
    import { userStore } from "$lib/stores/user";
    import type { Offer, User } from "$lib/types";
    import { onDestroy } from "svelte";
    import type { PageData } from "./$types";

    export let data: PageData

    // WHAT THE FUCK IS GOING ON
    // navigating between slugs doesnt remount the page so <script> does not run a second time and state is persisted
    // https://github.com/sveltejs/kit/issues/1497
    let prevData: PageData|null = null
    $: ((data: PageData) => {
        if (prevData?.user?.id === data.user?.id) {
            // user id same = no navigation
            return
        }
        prevData = data
        updateDerivedVariables($userStore)
        resetState()
    })(data)

    let activeOffers: Offer[] = data.offers
    let isCurrentUser = false
    let user: User|null = data.user

    const updateDerivedVariables = (store: typeof $userStore) => {
        user = data.user
        activeOffers = data.offers.filter(o=>o.status===0)
        if (store.user && data.user?.id === store.user.id) {
            user = store.user
            isCurrentUser = true
        } else {
            isCurrentUser = false
        }
    }
    onDestroy(userStore.subscribe(updateDerivedVariables))
    const resetState = () => {
        showInactiveOffers = false
        isEditingUsername = false
    }

    let showInactiveOffers = false
    const handleShowInactiveOffersToggle = () => {
        showInactiveOffers = !showInactiveOffers
    }

    let newUsername = ''
    let isEditingUsername = false
    let isSavingUsername = false    
    const handleUsernameEditorToggle = () => {
        isEditingUsername = !isEditingUsername
        newUsername = (user?.username) ?? ''
    }
    const handleUsernameSave = async () => {
        isSavingUsername = true
        try {
            const newUser = await changeUsername(newUsername)
            userStore.set({...$userStore, user: newUser})
            handleUsernameEditorToggle()
        } catch (err) {
            console.error(err)
            $errorStore.addError('Failed to edit username: ' + err)
        }
        isSavingUsername = false
    }

    let fileInputEl: HTMLInputElement
    let isSavingAvatar = false
    const handleEditClick = () => {
        fileInputEl.click()
    }
    const handleDeleteClick = () => {
        _updateAvatar(null)
    }
    const handleFileInput = async () => {
        const file = fileInputEl?.files![0]
        _updateAvatar(file)
    }
    const _updateAvatar = async (file: File|null) => {
        isSavingAvatar = true
        
        try {
            const user = await changeAvatar(file)
            // avatar overriden because browser might attempt to load image from server before it is accessible so we just use local file
            userStore.set({
                ...$userStore,
                user
            })
        } catch (err) {
            console.error(err)
            $errorStore.addError(`There was an error ${file ? 'saving' : 'removing'} the avatar. Check console for details.`)
        }

        isSavingAvatar = false
    }

</script>

<style lang="scss">
    .page-container {
        display: flex;
        align-items: center;
        flex-direction: column;
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        margin-top: 10px;
    }
    .content-container {
        width: 100%;
        max-width: 1024px;
        margin-left: 0;
        margin-right: 0;
    }
    .username-container {
        display: flex;
        height: 72px;
        .is-staff {
            color: red;
            text-transform: uppercase;
            margin-left: 16px;
        }
        input {
            margin-top: auto;
            margin-bottom: auto;
        }
        button {
            margin-top: auto;
            margin-bottom: auto;
            margin-left: 2px;
        }
    }
    .edit-icon {
        height: 20px;
        align-self: center;
        margin-left: 10px;
        cursor: pointer;
    }
    .contact-info {
        display: flex;
    }
    .contact-icon {
        height: 25px;
        margin-right: 8px;
    }
    .inactive-toggle {
        font-weight: 300;
        cursor: pointer;
    }
    .user-avatar {
        object-fit: cover;
        height: 120px;
        width: 120px;
        border-radius: 50%;
    }
</style>

<svelte:head>
    <title>{user?.username ?? '404'} | {SITE_TITLE}</title>
</svelte:head>

<div class="page-container">
    <div class="content-container">
        {#if user}
            <div class="user-avatar-container">
                <img class="user-avatar" src={user?.avatar ?? NO_IMAGE_PHOTO.url} alt={`${user?.username}'s avatar'`}>
                {#if isCurrentUser}
                    <button on:click={handleEditClick} disabled={isSavingAvatar}>edit</button>
                    <button on:click={handleDeleteClick} disabled={isSavingAvatar}>delete</button>
                {/if}
                <input style="display: none;" id="file-upload" type="file" name="Photos" accept="image/*" bind:this={fileInputEl} on:change={handleFileInput}>
            </div>
            <div class="username-container">
                {#if isEditingUsername}
                    <input disabled={isSavingUsername} type="text" placeholder="username" bind:value={newUsername}>
                    <button on:click={handleUsernameEditorToggle} disabled={isSavingUsername}>✕</button>
                    <button on:click={handleUsernameSave} disabled={isSavingUsername || newUsername.length === 0}>💾</button>
                {:else}
                    <h2>{user?.username}</h2>
                    {#if isCurrentUser}
                        <img class="edit-icon" src="/assets/edit-icon.svg" alt="Change your username" on:click={handleUsernameEditorToggle} on:keypress={handleUsernameEditorToggle}>
                    {/if}
                {/if}

                {#if user.isStaff}
                    <h2 class="is-staff">staff</h2>
                {/if}
            </div>
            <p class="contact-info">
                <img class="contact-icon" src="/assets/mail-icon.svg" alt="Email">
                <a href={`mailto:${user.email}`}>{user.email}</a>
            </p>
            <p class="contact-info">
                <img class="contact-icon" src="/assets/phone-icon.svg" alt="Phone number">
                {user.phoneNumber ?? 'Not provided'}
            </p>
            <h3>
                {showInactiveOffers ? 'All ' : ''}{user.username}'s offers ({showInactiveOffers ? data.offers.length : activeOffers.length}): 
                {#if isCurrentUser || $userStore.user?.isStaff}
                    <span class="inactive-toggle" on:click={handleShowInactiveOffersToggle} on:keypress={handleShowInactiveOffersToggle}>{showInactiveOffers ? 'Hide' : 'Show'} inactive offers</span>
                {/if}
            </h3>
            {#if (showInactiveOffers ? data.offers : activeOffers).length > 0}
                <OfferGrid offers={showInactiveOffers ? data.offers : activeOffers} />
            {:else}
                <p>No offers :(</p>
            {/if}
        {:else}
            <h2>404</h2>
        {/if}
    </div>
</div>