import { browser } from '$app/environment'
import { env } from '$env/dynamic/public'
import { validateOffer, validateOffers, validateUser, type Offer, type User } from './types'

export const BASE_URL = env.PUBLIC_API_URL
// SSR fetch resolves localhost to [::1] which doesnt work with django instead of 127.0.0.1, stupid
//if (!browser) BASE_URL = BASE_URL.replace('localhost', '127.0.0.1')
// alternatively, run django with --ipv6 flag

/* Helper functions */

const getCookie = (name: string) => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop()!.split(';').shift()
}

const authedFetch = async ({
    url,
    method,
    jsonBody,
    formData,
    fetchFn,
}: {
    url: string
    method: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE'
    jsonBody?: string
    formData?: FormData
    fetchFn?: typeof fetch
}) => {
    if (!fetchFn) fetchFn = fetch

    const headers: HeadersInit = {}
    if (jsonBody) {
        headers['Content-Type'] = 'application/json'
    }
    if (browser) {
        const csrfToken = getCookie('csrftoken')
        if (csrfToken) headers['X-CSRFToken'] = csrfToken
    }

    const fetchBaseUrl = (browser ? env.PUBLIC_API_URL : env.PUBLIC_API_URL__SERVER)!

    const res = await fetchFn(`${fetchBaseUrl}/api${url}`, {
        credentials: 'include',
        method,
        body: jsonBody || formData,
        headers,
    })

    let data: any = undefined
    try {
        data = await res.json()
    } catch (err) {}

    return {
        status: res.status,
        ok: res.ok,
        data,
    }
}

/* Users */

export const fetchUser = async (userId: number | 'me', fetchFn?: typeof fetch): Promise<User | null> => {
    const { status, ok, data } = await authedFetch({
        url: `/users/${userId}`,
        method: 'GET',
        fetchFn,
    })
    if (status === 404) return null
    if (!ok) throw new Error(JSON.stringify(data))

    try {
        return validateUser(data)
    } catch (err) {
        throw err
    }
}

export const changeUsername = async (username: string): Promise<User> => {
    const { ok, data } = await authedFetch({
        url: '/users/me/username/',
        method: 'PATCH',
        jsonBody: JSON.stringify({ username }),
    })

    if (!ok) throw new Error(JSON.stringify(data))

    return validateUser(data)
}

export const changeAvatar = async (file: File | null) => {
    const payload = new FormData()
    if (file) payload.append('avatar', file, file.name)

    const { ok, data } = await authedFetch({
        url: '/users/me/avatar/',
        method: file ? 'PATCH' : 'DELETE',
        formData: file ? payload : undefined,
    })

    if (!ok) throw new Error(JSON.stringify(data))

    return validateUser(data)
}

/* Auth */

export const login = async (email: string, password: string): Promise<void> => {
    const { ok, data } = await authedFetch({
        url: '/auth/login/',
        method: 'POST',
        jsonBody: JSON.stringify({ email, password }),
    })
    if (!ok) {
        throw new Error(JSON.stringify(data))
    }
}

export const logout = async () => {
    const { ok, data } = await authedFetch({
        url: '/auth/logout/',
        method: 'POST',
    })
    if (!ok) throw new Error(JSON.stringify(data))
}

export const register = async ({ email, password, username, phoneNumber }: { email: string; password: string; username?: string; phoneNumber?: string }) => {
    const { ok, data } = await authedFetch({
        url: '/auth/register/',
        method: 'POST',
        jsonBody: JSON.stringify({ email, password, username, phoneNumber }),
    })
    if (!ok) throw new Error(JSON.stringify(data))
}

/* Offers */

export const fetchOffers = async (params: URLSearchParams, fetchFn: typeof fetch): Promise<Offer[]> => {
    const { data } = await authedFetch({
        url: `/offers/?${params.toString()}`,
        method: 'GET',
        fetchFn,
    })

    return validateOffers(data)
}

export const fetchOffer = async (offerId: string, fetchFn: typeof fetch): Promise<Offer | null> => {
    const { status, data } = await authedFetch({
        url: `/offers/${offerId}`,
        method: 'GET',
        fetchFn,
    })
    if (status === 404) return null

    return validateOffer(data)
}

export const createOffer = async ({
    title,
    description,
    category,
    type,
    squareMeters,
    price,
    cityName,
    streetName,
    houseNumber,
    apartmentNumber,
    photos,
}: {
    title: string
    description?: string
    category: number
    type: number
    squareMeters?: number
    price?: number
    cityName: string
    streetName?: string
    houseNumber?: string
    apartmentNumber?: string
    photos: File[]
}) => {
    const payload = new FormData()
    payload.append('title', title)
    if (description) payload.append('description', description)
    payload.append('category', category.toString())
    payload.append('type', type.toString())
    if (squareMeters) payload.append('square_meters', squareMeters.toString())
    if (price) payload.append('price', price.toString())
    payload.append('city', cityName)
    if (streetName) payload.append('street_name', streetName)
    if (houseNumber) payload.append('house_number', houseNumber)
    if (apartmentNumber) payload.append('apartment_number', apartmentNumber)
    for (let photo of photos) {
        payload.append('photos', photo, photo.name)
    }

    const { ok, data } = await authedFetch({
        url: '/offers/',
        method: 'POST',
        formData: payload,
    })
    if (!ok) throw new Error(JSON.stringify(data))
    if (typeof data === 'object' && typeof data.id === 'number') {
        return data.id as number
    }
    throw new Error('create offer response validation fail')
}

export const getRandomOffers = async () => {
    const { ok, data } = await authedFetch({
        url: '/offers/suggested',
        method: 'GET',
    })
    if (!ok) throw new Error(JSON.stringify(data))

    return validateOffers(data)
}

export const changeOfferStatus = async (offerId: number, newStatus: 0 | 1) => {
    const { ok, data } = await authedFetch({
        url: `/offers/${offerId}/status`,
        method: 'PATCH',
        jsonBody: JSON.stringify({ status: newStatus }),
    })
    if (!ok) throw new Error(JSON.stringify(data))

    return validateOffer(data)
}
