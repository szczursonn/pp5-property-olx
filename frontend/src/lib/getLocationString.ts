import type { Offer } from "./types"

export const getLocationString = (offer: Offer): string => {
    let str = offer.locationCityName
    if (offer.locationStreetName) str+=', '+offer.locationStreetName
    if (offer.locationHouseNumber) str+=' '+offer.locationHouseNumber
    if (offer.locationAptNumber) str+=' '+offer.locationAptNumber
    return str
}