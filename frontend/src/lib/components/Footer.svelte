<script lang="ts">
    import { GITHUB_REPO_URL, SITE_TITLE } from "$lib/constants";
</script>

<style lang="scss">
    $footer-height: 120px;

    footer {
        width: 100%;
        height: $footer-height;
        box-shadow: 0px 0px 10px grey;
        color: var(--navbar-text-color);
        background-color: var(--navbar-bg-color);
        display: flex;
        flex-direction: column;
        align-items: center;
        a img {
            height: 50px;
            filter: invert(100%);
            &:hover {
                filter: invert(100%) brightness(120%);
            }
        }
    }
</style>

<footer>
    <p>{SITE_TITLE.toUpperCase()}</p>
    <a href={GITHUB_REPO_URL}>
        <img src="/assets/github-mark.svg" alt="Github icon">
    </a>
</footer>