import { GITHUB_REPO_URL, OFFER_CATEGORIES } from "$lib/constants"

type Options = ({
    name: string,
    url: string,
    shouldPreload: boolean
} | {
    name: string,
    suboptions: {
        name: string,
        url: string
    }[],
    shouldPreload: boolean
})[]

const options: Options = [
    {
        name: 'Offers',
        suboptions: OFFER_CATEGORIES.map(({value, label}) => {
            return {name: label, url: `/offers?category=${value}`}
        }),
        shouldPreload: false
    }, {
        name: 'About',
        url: GITHUB_REPO_URL,
        shouldPreload: true
    }
]

export default options