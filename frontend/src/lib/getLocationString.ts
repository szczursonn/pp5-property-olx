import type { Offer } from "./types"

export const getLocationString = (offer: Offer): string => {
    let str = offer.location.city
    if (offer.location.street) str+=', '+offer.location.street
    if (offer.location.house) str+=' '+offer.location.house
    if (offer.location.apt) str+=' '+offer.location.apt
    return str
}