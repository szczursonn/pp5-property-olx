export type User = {
    id: number,
    username: string,
    email: string,
    phoneNumber: string|null,
    isStaff: boolean
}

export type Offer = {
    id: number,
    title: string,
    description: string|null,
    type: number,
    status: number,
    category: number,
    squareMeters: number|null,
    price: number|null,
    locationLat: number,
    locationLng: number,
    locationCityName: string,
    locationStreetName: string|null,
    locationHouseNumber: string|null,
    locationAptNumber: string|null,
    authorId: number,
    createdAt: Date,
    photos: {
        id: number,
        photo: string
    }[]
}
