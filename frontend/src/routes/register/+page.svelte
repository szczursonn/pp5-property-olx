<script lang="ts">
    import { register } from "$lib/api";
    import { SITE_TITLE } from "$lib/constants";
    import { errorStore } from "$lib/stores/error";

    let email = ''
    let password = ''
    let username = ''
    let phoneNumber = ''
    let isLoading = false

    const handleSubmit = async () => {
        isLoading=true
        try {
            await register({
                email,
                password,
                username: username.length > 0 ? username : undefined,
                phoneNumber: phoneNumber.length > 0 ? phoneNumber : undefined
            })
            // refresh the page
            window.location.href = '/'
        } catch (err) {
            console.error(err)
            $errorStore.addError(`Failed to register. Check console for details.`)
        }
        isLoading=false
    }
</script>

<svelte:head>
    <title>Register | {SITE_TITLE}</title>
</svelte:head>

<style lang="scss">
    .register-form-container {
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
    .login-link {
        color: blueviolet;
        &:hover {
            filter: brightness(120%);
        }
    }
    .additional-text {
        margin: 0;
        font-size: small;
        opacity: 0.9;
    }
</style>

<div class="register-form-container">
    <form on:submit|preventDefault={handleSubmit}>
        <h2>Sign up</h2>
        
        <label for="login-input-email">Email</label>
        <input class="text-input" bind:value={email} id="login-input-email" type="text" required={true} disabled={isLoading}>

        <label for="login-input-password">Password</label>
        <input class="text-input" bind:value={password} id="login-input-password" type="password" required={true} disabled={isLoading}>

        <label for="login-input-username">
            Username
            <p class="additional-text">Optional, defaults to email</p>
        </label>
        <input class="text-input" bind:value={username} id="login-input-username" type="text" disabled={isLoading}>

        <label for="login-input-phone">
            Phone number
            <p class="additional-text">Optional</p>
        </label>
        
        <input class="text-input" bind:value={phoneNumber} id="login-input-phone" type="text" disabled={isLoading}>

        <input type="submit" value="Register" disabled={isLoading || email.length === 0 || password.length === 0}>
        <p>Already have an account? <a class="login-link" href="/login">Login here</a></p>
    </form>
</div>