import { fetchOffer, fetchUser } from "$lib/api";
import type { PageLoad } from "./$types"

export const load = (async ({params, fetch}) => {
    const offerId = params.slug
    const offer = await fetchOffer(offerId, fetch)
    const author = (await fetchUser(offer.authorId, fetch))!
    return {
        offer,
        author
    }
}) satisfies PageLoad;