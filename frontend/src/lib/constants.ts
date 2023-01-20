import type { Offer } from "./types"

export const OFFER_CATEGORIES = [
    {value: 0, label: 'House'},
    {value: 1, label: 'Plot'},
    {value: 2, label: 'Apartment'},
    {value: 3, label: 'Room'},
    {value: 4, label: 'Garage or Parking'},
    {value: 5, label: 'Business Premises'},
    {value: 6, label: 'Warehouse'},
    {value: 7, label: 'Other'}
]

export const OFFER_TYPES = [
    {value: 0, label: 'Rent'},
    {value: 1, label: 'Purchase'}
]

export const OFFER_STATUSES = [
    {value: 0, label: 'Active'},
    {value: 1, label: 'Inactive'}
]

export const NO_IMAGE_PHOTO: Offer['photos'][0] = {id: -1, url: "/assets/no-photo.jpg"}

export const SITE_TITLE = 'property auction app'
export const GITHUB_REPO_URL = 'https://github.com/szczursonn/pp5-property-olx'