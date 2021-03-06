//import hexmap from './map'
let _ = require('lodash')

export function hexParse(hex) {
    let hexList = hex.match(/.{1,2}/g)
    if (isValidHexProperty(hex) === false) {
        throw Error('Invalid hex code.')
    }
    let hexChallenge = {
        "terrain": {
            "type": hexList[0].charAt(0),
            "challenge": _.toNumber(hexList[0].charAt(1))
        },
        "resource": {
            "type": hexList[1].charAt(0),
            "challenge": _.toNumber(hexList[1].charAt(1))
        },
        "encounter": {
            "type": hexList[2].charAt(0),
            "challenge": _.toNumber(hexList[2].charAt(1))
        },
        "location": {
            "type": hexList[3].charAt(0),
            "challenge": _.toNumber(hexList[3].charAt(1))
        },
        "treasure": {
            "type": hexList[4].charAt(0),
            "challenge": _.toNumber(hexList[4].charAt(1))
        }
    }
    return hexChallenge
}

export function isValidHexProperty(hex) {
    let hexList = hex.match(/.{1,2}/g)
    let isValid = true
    if (hexList.length !== 5) {
        isValid = false
    }
    hexList.forEach(prop => {
        const key = prop.charAt(0)
        const val = _.toNumber(prop.charAt(1))
        if (key.length !== 1 && key.match(/[^a-zA-Z]/)) {
            isValid = false
        }

        if (Number.isInteger(val) === false) {
            isValid = false
        }
    })
    return isValid
}

export function partyBonus(party) {
    let combat = 0,
        exploration = 0,
        diplomacy = 0,
        travel = 0
    party.forEach(member => {
        if (member == 'Warrior') {
            combat += 2
            exploration += 1
        }

        if (member == 'Guide') {
            exploration += 2
            diplomacy += 1
        }

        if (member == 'Merchant') {
            diplomacy += 2
            combat += 1
        }

        if (member == 'Sorcerer') {
            combat += 1
            diplomacy += 1
            exploration += 1
        }
    })

    let baseEffort = {
        "combat": combat,
        "exploration": exploration,
        "diplomacy": diplomacy,
        "travel": travel
    }
    return baseEffort
}