import { expect } from 'chai'
import { partyBonus, hexParse } from '../src/index'

const party1 = ['Warrior', 'Guide', 'Merchant', 'Sorcerer']
const party2 = ['Warrior', 'Warrior']
const party3 = ['Guide', 'Merchant', 'Librarian', 'Merchant'] // there is no librarian
const party4 = []
const hexCode1 = "F3G6B5X0D9"
const hexCode2 = "F3G6B5"
const hexCode3 = "F3G6B5X0D9E5"

describe('Party Base Bonus', () => {
    it('outputs the correct base effort for a 4-member party of each class', () => {
        expect(partyBonus(party1)).to.eql({combat: 4, exploration: 4, diplomacy: 4, travel: 0})
    })
    it('outputs the correct base effort for party with duplicate classes', () => {
        expect(partyBonus(party2)).to.eql({combat: 4, exploration: 2, diplomacy: 0, travel: 0})
    })
    it('outputs the correct base effort for party with an invalid class', () => {
        expect(partyBonus(party3)).to.eql({combat: 2, exploration: 2, diplomacy: 5, travel: 0})
    })
    it('outputs the correct base effort for an empty party', () => {
        expect(partyBonus(party4)).to.eql({combat: 0, exploration: 0, diplomacy: 0, travel: 0})
    })
})

describe('Hex Parser', () => {
    it('returns the correct hex challenge object for a given code', () => {
        expect(hexParse(hexCode1)).to.eql({"terrain": {"type": "F", "challenge": 3},"resource": {"type": "G", "challenge": 6},"encounter": {"type": "B", "challenge": 5},"location": {"type": "X", "challenge": 0},"treasure": {"type": "D", "challenge": 9}})
    })
    it('throws an error if hex code is too short', () => {
        expect(() => hexParse(hexCode2)).to.throw(Error)
    })
    it('throws an error if hex code is too long', () => {
        expect(() => hexParse(hexCode3)).to.throw(Error)
    })
})