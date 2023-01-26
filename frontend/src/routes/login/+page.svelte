<script lang="ts">
    import { goto } from '$app/navigation'
    import { login } from '$lib/api'
    import { SITE_TITLE } from '$lib/constants'
    import { errorStore } from '$lib/stores/error'
    import { userStore } from '$lib/stores/user'

    let email = ''
    let password = ''
    let isLoading = false
    let wasWrongCredentials = false

    const handleSubmit = async () => {
        isLoading = true
        wasWrongCredentials = false
        try {
            await login(email, password)
            window.location.href = '/'
        } catch (err) {
            console.error(err)
            if (String(err).includes('Wrong email or password')) {
                wasWrongCredentials = true
            } else {
                $errorStore.addError(`Failed to login. Check console for details.`)
            }
        }
        isLoading = false
    }

    userStore.subscribe(({ user }) => {
        if (user) {
            goto('/')
        }
    })
</script>

<svelte:head>
    <title>Log in | {SITE_TITLE}</title>
</svelte:head>

<div class="login-form-container">
    <form on:submit|preventDefault={handleSubmit}>
        <h2>Sign in</h2>
        <label for="login-input-login">Email</label>
        <input class="text-input" bind:value={email} id="login-input-login" type="text" disabled={isLoading} />
        <label for="login-input-password">Password</label>
        <input class="text-input" bind:value={password} id="login-input-password" type="password" disabled={isLoading} />
        <input type="submit" value="Log in" disabled={isLoading || email.length === 0 || password.length === 0} />
        {#if wasWrongCredentials}
            <p class="error-text">Wrong email or password. Re-enter them and try again.</p>
        {/if}
        <p>Don't have an account? <a class="register-link" href="/register">Register here</a></p>
    </form>
</div>

<style lang="scss">
    .login-form-container {
        margin-top: 2%;
    }
    form {
        display: flex;
        flex-direction: column;
        margin-left: auto;
        margin-right: auto;
        max-width: 320px;
    }
    .text-input {
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
    }
    .register-link {
        color: blueviolet;
        &:hover {
            filter: brightness(120%);
        }
    }
    .error-text {
        color: red;
    }
</style>
