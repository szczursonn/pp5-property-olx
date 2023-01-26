import { fetchOffer, fetchUser } from '$lib/api'
import type { PageLoad } from './$types'

export const load = (async ({ params, fetch }) => {
    const offerId = params.slug
    const offer = await fetchOffer(offerId, fetch)
    const author = offer ? (await fetchUser(offer.authorId, fetch))! : null
    return {
        offer,
        author,
    }
}) satisfies PageLoad
