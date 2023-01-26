import { fetchOffers, fetchUser } from '$lib/api'
import type { PageLoad } from './$types'

export const load = (async ({ params, fetch }) => {
    const userId = params.slug
    const user = await fetchUser(parseInt(userId), fetch)
    const offers = await fetchOffers(new URLSearchParams({ author_id: userId }), fetch)
    return {
        user,
        offers,
    }
}) satisfies PageLoad
