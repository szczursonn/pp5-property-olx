import type { PageServerLoad } from './$types'

export const load = (() => {
    return {
        backgroundImageId: (Math.round(Math.random() * 10000) % 5) + 1,
    }
}) satisfies PageServerLoad
