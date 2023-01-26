import { BASE_URL } from './api'
import { OFFER_CATEGORIES, OFFER_STATUSES, OFFER_TYPES } from './constants'

export class ValidationError extends Error {
    constructor(public object: 'user' | 'offer') {
        super(`Validation of object ${object} failed`)
        this.name = 'ValidationError'
    }
}

export type User = {
    id: number
    username: string
    email: string
    phoneNumber: string | null
    isStaff: boolean
    avatar: string | null
}

export const validateUser = (data: any): User => {
    if (
        typeof data === 'object' &&
        data !== null &&
        typeof data.id === 'number' &&
        typeof data.username === 'string' &&
        typeof data.email === 'string' &&
        (typeof data.phone_number === 'string' || data.phone_number === null) &&
        typeof data.is_staff === 'boolean' &&
        (typeof data.avatar === 'string' || data.avatar === null)
    ) {
        if (typeof data.avatar === 'string' && !data.avatar.startsWith('http')) {
            data.avatar = BASE_URL + data.avatar
        }
        return {
            id: data.id,
            username: data.username,
            email: data.email,
            phoneNumber: data.phone_number,
            isStaff: data.is_staff,
            avatar: data.avatar,
        } as User
    }
    throw new ValidationError('user')
}

export type Offer = {
    id: number
    title: string
    description: string | null
    type: number
    typeString: string
    status: number
    statusString: string
    category: number
    categoryString: string
    squareMeters: number | null
    price: number | null
    location: {
        lat: number
        lng: number
        city: string
        street: string | null
        house: string | null
        apt: string | null
    }
    authorId: number
    createdAt: Date
    photos: {
        id: number
        url: string
    }[]
    activeUntil: Date
}

export const validateOffer = (data: any): Offer => {
    if (
        typeof data === 'object' &&
        typeof data.id === 'number' &&
        typeof data.title === 'string' &&
        (typeof data.description === 'string' || data.description === null) &&
        typeof data.type === 'number' &&
        typeof data.status === 'number' &&
        typeof data.category === 'number' &&
        (typeof data.square_meters === 'number' || data.square_meters === null) &&
        (typeof data.price === 'number' || data.price === null) &&
        typeof data.location_lat === 'number' &&
        typeof data.location_lng === 'number' &&
        typeof data.location_city_name === 'string' &&
        (typeof data.location_street_name === 'string' || data.location_street_name === null) &&
        (typeof data.location_house_number === 'string' || data.location_house_number === null) &&
        (typeof data.location_apt_number === 'string' || data.location_apt_number === null) &&
        typeof data.author_id === 'number' &&
        typeof data.created_at === 'string' &&
        data.photos instanceof Array &&
        data.photos.every((item: any) => typeof item === 'object' && typeof item.id === 'number' && typeof item.photo === 'string') &&
        typeof data.active_until === 'string'
    ) {
        // django generic api view returns absolute url but regular api view doesnt, nice
        for (let item of data.photos) {
            if (typeof item.photo === 'string' && !item.photo.startsWith('http')) {
                item.photo = BASE_URL + item.photo
            }
        }
        return {
            id: data.id,
            title: data.title,
            description: data.description,
            type: data.type,
            get typeString() {
                return OFFER_TYPES.find((t) => t.value === this.type)?.label ?? 'Unknown type'
            },
            status: data.status,
            get statusString() {
                return OFFER_STATUSES.find((s) => s.value === this.status)?.label ?? 'Unknown status'
            },
            category: data.category,
            get categoryString() {
                return OFFER_CATEGORIES.find((c) => c.value === this.category)?.label ?? 'Unknown category'
            },
            squareMeters: data.square_meters,
            price: data.price,
            location: {
                lat: data.location_lat,
                lng: data.location_lng,
                city: data.location_city_name,
                street: data.location_street_name,
                house: data.location_house_number,
                apt: data.location_apt_number,
            },
            authorId: data.author_id,
            createdAt: new Date(data.created_at),
            photos: data.photos.map((item: any) => {
                return {
                    id: item.id,
                    url: item.photo,
                }
            }),
            activeUntil: new Date(data.active_until),
        } as Offer
    }
    throw new ValidationError('offer')
}

export const validateOffers = (data: any): Offer[] => {
    if (data instanceof Array) {
        return data.map((item) => validateOffer(item))
    }
    throw new ValidationError('offer')
}
