<script lang="ts">
    import { errorStore } from "$lib/stores/error";

    const handleClose = () => {
        $errorStore.clearErrors()
    }
    
</script>

<style lang="scss">
    .modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0,0,0);
        background-color: rgba(0,0,0,0.4);
        &.show {
            display: block;
        }
    }
    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 40%;
        position: relative;
    }
    .error {
        color: red;
    }
    .close-btn {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        &:hover, &:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
    }

</style>

<div class="modal" class:show={$errorStore.errors.length>0}>
    <div class="modal-content">
        <span class="close-btn" on:click={handleClose} on:keypress={handleClose}>×</span>
        <h3>{$errorStore.errors.length>1 ? `There were ${$errorStore.errors.length} errors:` : 'There was an error: '}</h3>
        {#each $errorStore.errors as error, i}
            <p class="error">{$errorStore.errors.length>1 ? `${i+1}. ` : ''}{error}</p>
        {/each}
    </div>
</div>