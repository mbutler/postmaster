/**
 * This module handles creating the hex grid and individual hex methods
 * @module Map
 * @namespace
 */

let SVG = require('svg.js')
let Honeycomb = require('honeycomb-grid')
let _ = require('lodash')
let config = require('./config')

const draw = SVG(config.map.divContainer)

const Hex = Honeycomb.extendHex({
    size: config.map.hexSize,
    orientation: 'flat',
    render(draw) {
        const { x, y } = this.toPoint()
        const corners = this.corners()
        this.screenCoords = { 'x': x, 'y': y }
        this.cornerList = this.corners().map(corner => this.toPoint().add(corner))
        this.selected = false
        this.resources = generateResources()

        this.draw = draw
            .polygon(corners.map(({ x, y }) => `${x},${y}`))
            .fill(randomColor(this.resources))
            .stroke({ width: 1, color: '#E0E0E0' })
            .translate(x, y)
    },
    highlight() {
        if (this.selected === true) {
            this.selected = true
            this.draw
                .fill({ opacity: 1, color: 'aquamarine' })
                
        } else {
            this.selected = false
            this.draw
                .fill({ opacity: 0, color: 'none' })
        }
    }
})

const Grid = Honeycomb.defineGrid(Hex)

const grid = Grid.rectangle({
    width: config.map.width,
    height: config.map.height,
    onCreate(hex) {
        hex.render(draw)
    }
})

function randomColor(resources) {
    let social = resources.t
    let val = social.toString()
    let greyScale = {"0": "#FFFFFF", "1": "#E8E8E8", "2": "#D0D0D0", "3": "#B0B0B0", "4": "#808080", "5": "#909090", "6": "#686868", "7": "#383838", "8": "#000000" }
    let color = greyScale[val]
    console.log(color)
    return color
    
    // return '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0')
}

function generateResources(resources) {
    let travel = Math.floor(Math.random() * 9)
    let exploration = Math.floor(Math.random() * 9)
    let social = Math.floor(Math.random() * 9)
    let combat = Math.floor(Math.random() * 9)
    return {t: travel, e: exploration, s: social, c: combat}
}

console.log(grid[0])