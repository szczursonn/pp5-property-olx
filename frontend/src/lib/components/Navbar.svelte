<script lang="ts">
    import { goto } from '$app/navigation'
    import { BASE_URL, logout } from '$lib/api'
    import clickOutside from '$lib/clickOutside'
    import { NO_IMAGE_PHOTO, SITE_TITLE } from '$lib/constants'
    import { userStore } from '$lib/stores/user'
    import LoadingSpinner from './LoadingSpinner.svelte'
    import options from './NavbarData'

    let selectedIndex = -1
    let isMyAccountSelected = false
    let isDrawerOpened = false

    const onOptionSelect = (newSelectedIndex: number) => {
        if (selectedIndex === newSelectedIndex) {
            selectedIndex = -1
        } else {
            selectedIndex = newSelectedIndex
        }
    }

    const openDrawer = () => (isDrawerOpened = true)
    const closeDrawer = () => {
        selectedIndex = -1
        isMyAccountSelected = false
        isDrawerOpened = false
    }
    const handleMyAccountClick = () => {
        if ($userStore.user) {
            isMyAccountSelected = !isMyAccountSelected
        } else {
            closeDrawer()
            goto('/login')
        }
    }
    const handleLogout = async () => {
        await logout()
        window.location.reload()
    }
</script>

<header use:clickOutside={closeDrawer}>
    <nav>
        <a class="site-title" href="/">
            {SITE_TITLE}
        </a>
        <div class="navbar-options-container" class:drawer-opened={isDrawerOpened}>
            <img class="drawer-close-btn" src="/assets/plus-icon.svg" alt="Plus icon" on:click={closeDrawer} on:keypress={closeDrawer} />
            <ul class="navbar-dropdowns-container" use:clickOutside={() => onOptionSelect(-1)}>
                {#each options as option, i}
                    <li data-sveltekit-preload-data={option.shouldPreload ? 'hover' : 'tap'} class="navbar-dropdown" class:selected={i === selectedIndex}>
                        {#if 'url' in option}
                            <a class="navbar-dropdown-text" href={option.url} on:click={closeDrawer}>{option.name}</a>
                        {:else}
                            <p class="navbar-dropdown-text" on:click={() => onOptionSelect(i)} on:keypress={() => onOptionSelect(i)}>
                                {option.name}
                                <span class="list-triangle-icon" class:selected={i === selectedIndex} />
                            </p>
                            <ul class="navbar-dropdown-items-container" class:visible={i === selectedIndex}>
                                {#each option.suboptions as suboption}
                                    <li class="navbar-dropdown-item">
                                        <a class="navbar-dropdown-item-text" href={suboption.url} on:click={closeDrawer}>{suboption.name}</a>
                                    </li>
                                {/each}
                            </ul>
                        {/if}
                    </li>
                {/each}
            </ul>
            <hr />
            <div class="my-account-btn-container">
                <a class="my-account-btn" href="/login" on:click|preventDefault={handleMyAccountClick} use:clickOutside={() => (isMyAccountSelected = false)}>
                    {#if $userStore.loading}
                        <LoadingSpinner />
                    {:else}
                        <img src="/assets/user-profile-icon.svg" alt="User profile icon" />
                        <div>My account</div>
                    {/if}
                </a>
                <ul class="navbar-dropdown-items-container" class:visible={isMyAccountSelected}>
                    <li class="navbar-dropdown-item account-dropdown-item">
                        <img class="user-avatar" src={$userStore.user?.avatar ?? NO_IMAGE_PHOTO.url} alt={`${$userStore.user?.username}'s avatar'`} />
                        <a class="account-username" href={`/users/${$userStore.user?.id}`}>{$userStore.user?.username}</a>
                        <p class="account-email">{$userStore.user?.email}</p>
                    </li>
                    {#if $userStore?.user?.isStaff}
                        <li class="navbar-dropdown-item">
                            <a class="navbar-dropdown-item-text" href={`${BASE_URL}/admin`}>Admin panel</a>
                        </li>
                    {/if}
                    <li class="navbar-dropdown-item">
                        <p class="navbar-dropdown-item-text" on:click={handleLogout} on:keypress={handleLogout}>Logout</p>
                    </li>
                </ul>
            </div>
            <hr />
            <a class="add-offer-btn" href="/offers/new" on:click={closeDrawer}>
                <div>Add offer</div>
                <img src="/assets/plus-icon.svg" alt="Plus icon" />
            </a>
        </div>
        <div class="drawer-open-btn-container" on:click={openDrawer} on:keypress={openDrawer}>
            <img class="drawer-open-btn" src="/assets/drawer-icon.svg" alt="Drawer open icon" />
        </div>
    </nav>
</header>

<style lang="scss">
    $breakpoint-icons: 1050px;
    $breakpoint-drawer: 600px;
    $navbar-height: 60px;

    header {
        position: sticky;
        top: 0px;
        width: 100%;
        height: $navbar-height;
        box-shadow: 0px 0px 3px grey;
        color: var(--navbar-text-color);
        background-color: var(--navbar-bg-color);
    }
    nav {
        display: flex;
        align-items: center;
        margin-left: auto;
        margin-right: auto;
        max-width: 1024px;
    }
    hr {
        display: none;
    }
    .navbar-options-container {
        display: flex;
        align-items: center;
        width: 100%;
    }
    .navbar-dropdowns-container {
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        margin-right: auto;
    }
    .navbar-dropdown {
        position: relative;
        transition: backdrop-filter 250ms;
        &:hover,
        &:focus {
            cursor: pointer;
            backdrop-filter: brightness(120%);
        }
        &.selected {
            backdrop-filter: brightness(90%);
        }
    }
    .navbar-dropdown-text {
        display: block;
        padding: 20px 8px;
        margin: 0;
    }
    .navbar-dropdown-item-text {
        @extend .navbar-dropdown-text;
        padding: 8px;
        transition: color 150ms;
        &:hover {
            color: var(--cta);
            cursor: pointer;
        }
    }
    .navbar-dropdown-items-container {
        display: none;
        position: absolute;
        top: 100%;
        left: 0px;
        padding-left: 0;
        margin-top: 0px;
        list-style: none;
        color: black;
        background-color: white;
        box-shadow: 0px 0px 5px grey;
        &.visible {
            display: inherit;
        }
    }
    .site-title {
        font-size: large;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .my-account-btn {
        display: flex;
        align-items: center;
        height: $navbar-height;
        white-space: nowrap;
        transition: backdrop-filter 250ms;
        padding-left: 10px;
        padding-right: 10px;
        &:hover,
        &:focus {
            cursor: pointer;
            backdrop-filter: brightness(120%);
        }
        img {
            width: 20px;
            margin-right: 10px;
            filter: invert(100%);
        }
    }
    .my-account-btn-container {
        position: relative;
    }
    .add-offer-btn {
        max-height: 24px;
        padding: 10px 20px;
        border-radius: 5px;
        margin-left: 20px;
        background-color: var(--cta);
        transition: filter 250ms;
        &:hover,
        &:focus {
            cursor: pointer;
            filter: brightness(120%);
        }
        img {
            display: none;
            width: 20px;
            filter: invert(100%);
        }
    }

    .drawer-open-btn-container {
        margin-left: auto;
    }
    .drawer-open-btn {
        display: none;
        filter: invert(100%);
    }
    .drawer-close-btn {
        display: none;
        height: 24px;
        position: relative;
        top: 10px;
        align-self: flex-end;
        z-index: 500;
        rotate: 45deg;
        cursor: pointer;
        filter: invert(100%);
    }
    .account-username {
        margin: 5px 20px;
        font-size: large;
        text-align: center;
    }
    .account-email {
        @extend .account-username;
        font-size: medium;
    }
    .account-dropdown-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    @media (max-width: $breakpoint-icons) and (min-width: $breakpoint-drawer) {
        nav {
            margin-left: 16px;
            margin-right: 16px;
        }
        .add-offer-btn {
            border-radius: 20px;
            div {
                display: none;
            }
            img {
                display: block;
            }
        }
        .my-account-btn div {
            display: none;
        }
    }

    @media (max-width: $breakpoint-drawer) {
        .drawer-open-btn {
            display: block;
        }
        .navbar-options-container {
            flex-direction: column;
            min-height: 100vh;
            width: auto;
            position: fixed;
            top: 0;
            right: -200px;
            z-index: 1000;
            padding-left: 10px;
            padding-right: 10px;
            background-color: var(--navbar-bg-color);
            box-shadow: 0px 0px 5px grey;
            transition: right 300ms;
        }
        .drawer-opened {
            right: 0;
        }
        .navbar-dropdowns-container {
            align-self: flex-start;
            align-items: flex-start;
            flex-direction: column;
            width: 100%;
            padding-left: 0px;
            margin-right: 0px;
        }
        .navbar-dropdown {
            align-self: flex-start;
            width: 100%;
            &:hover,
            &:focus {
                background-color: inherit;
            }
            &.selected {
                background-color: inherit;
            }
        }
        .navbar-dropdown-items-container {
            position: inherit;
            color: inherit;
            background-color: inherit;
            box-shadow: inherit;
        }
        .navbar-dropdown-item {
            margin-left: 10px;
        }
        .add-offer-btn {
            width: 100px;
            margin-top: 20px;
            margin-left: 0px;
        }
        header {
            display: flex;
        }
        nav {
            width: 100%;
            margin-left: 16px;
            margin-right: 16px;
        }
        .drawer-close-btn {
            display: block;
        }
        hr {
            display: inherit;
            align-self: stretch;
            margin: 0;
        }
    }

    .list-triangle-icon {
        display: inline-block;
        width: 0;
        height: 0;
        -webkit-transition: 0.25s -webkit-transform ease-in-out;
        transition: 0.25s transform ease-in-out;
        vertical-align: middle;
        border-top: 4px dashed;
        border-right: 4px solid transparent;
        border-left: 4px solid transparent;
        margin-left: 4px;
        &.selected {
            transform: rotate(-180deg);
        }
    }
    .user-avatar {
        object-fit: cover;
        height: 80px;
        width: 80px;
        border-radius: 50%;
    }
</style>
