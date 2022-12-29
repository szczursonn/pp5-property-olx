import { browser } from "$app/environment"
import { env } from "$env/dynamic/public";
import type { Offer, User } from "./types"

export const BASE_URL = env.PUBLIC_API_URL
// SSR fetch resolves localhost to [::1] which doesnt work with django instead of 127.0.0.1, stupid
//if (!browser) BASE_URL = BASE_URL.replace('localhost', '127.0.0.1')

const getCookie = (name: string) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift();
}

const authedFetch = ({url, method, jsonBody, formData, fetchFn}: {
    url: string,
    method: 'GET'|'POST'|'PATCH'|'PUT'|'DELETE',
    jsonBody?: string,
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
        if (csrfToken) headers['X-CSRFToken']=csrfToken
    }

    return fetchFn(`${BASE_URL}/${url}`, {
        credentials: 'include',
        method,
        body: jsonBody || formData,
        headers
    })
}

export const fetchUser = async (userId: number|'me', fetchFn?: typeof fetch): Promise<User|null> => {
    const res = await authedFetch({
        url: `api/users/${userId}`,
        method: 'GET',
        fetchFn
    })
    const data = await res.json()
    if (res.status === 404) return null
    if (!res.ok) throw new Error(JSON.stringify(data))

    data.phoneNumber=data.phone_number
    delete data.phone_number
    data.authorId=data.author_id
    delete data.author_id
    data.isStaff=data.is_staff
    delete data.is_staff

    return data as User
}

export const login = async (email: string, password: string) => {
    const res = await authedFetch({
        url: 'api/auth/login/',
        method: 'POST',
        jsonBody: JSON.stringify({email, password})
    })
    if (!res.ok) throw new Error(JSON.stringify(await res.json()))
}

export const logout = async () => {
    const res = await authedFetch({
        url: 'api/auth/logout/',
        method: 'POST'
    })
    if (!res.ok) throw new Error(JSON.stringify(await res.json()))
}

export const register = async ({email, password, username, phoneNumber}: {email: string, password: string, username?: string, phoneNumber?: string}) => {
    const res = await authedFetch({
        url: 'api/auth/register/',
        method: 'POST',
        jsonBody: JSON.stringify({email, password, username, phoneNumber})
    })
    if (!res.ok) throw new Error(JSON.stringify(await res.json()))
}

const camelcasifyOffer = (offer: any) => {
    offer.squareMeters = offer.square_meters
    delete offer.square_meters
    offer.locationLat = offer.location_lat
    delete offer.location_lat
    offer.locationLng = offer.location_lng
    delete offer.location_lng
    offer.locationCityName = offer.location_city_name
    delete offer.location_city_name
    offer.locationStreetName = offer.location_street_name
    delete offer.location_street_name
    offer.locationHouseNumber = offer.location_house_number
    delete offer.location_house_number
    offer.locationAptNumber = offer.location_apt_number
    delete offer.location_apt_number
    offer.authorId = offer.author_id
    delete offer.author_id
    offer.createdAt = offer.created_at
    delete offer.created_at

    offer.createdAt = new Date(offer.createdAt)
}

export const fetchOffers = async (params: URLSearchParams, fetchFn: typeof fetch) => {
    const res = await authedFetch({
        url: `api/offers/?${params.toString()}`,
        method: 'GET',
        fetchFn
    })
    const data = await res.json()

    // convert to camelcase
    for (let offer of data) {
        camelcasifyOffer(offer)
    }

    return data as Offer[]
}

export const fetchOffer = async (offerId: string, fetchFn: typeof fetch) => {
    const res = await authedFetch({
        url: `api/offers/${offerId}`,
        method: 'GET',
        fetchFn
    })
    const data = await res.json()
    camelcasifyOffer(data)
    return data as Offer
}

export const createOffer = async ({title, description, category, type, squareMeters, price, cityName, streetName, houseNumber, apartmentNumber, photos}: {
    title: string,
    description?: string,
    category: number,
    type: number,
    squareMeters?: number,
    price?: number,
    cityName: string,
    streetName?: string,
    houseNumber?: string,
    apartmentNumber?: string,
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

    const res = await authedFetch({
        url: 'api/offers/',
        method: 'POST',
        formData: payload
    })
    const data = await res.json()
    if (!res.ok) throw new Error(JSON.stringify(data))
    return data.id as number
}

export const getRandomOffers = async () => {
    const res = await authedFetch({
        url: 'api/offers/suggested',
        method: 'GET'
    })
    const data = await res.json()
    if (!res.ok) throw new Error(JSON.stringify(data))
    data.forEach(camelcasifyOffer)
    return data as Offer[]
}