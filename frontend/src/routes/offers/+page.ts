import { fetchOffers } from "$lib/api";
import type { PageLoad } from "./$types"

export const load = (async ({url, fetch}) => {
    const searchParams = url.searchParams
    if (!searchParams.has('category')) searchParams.set('category', '0')
    if (!searchParams.has('type')) searchParams.set('type', '0')
    return {
        offers: await fetchOffers(url.searchParams, fetch),
        params: url.searchParams
    }
}) satisfies PageLoad;