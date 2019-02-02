import { shallowMount } from '@vue/test-utils'
import { expect } from 'chai'

import BaseLogo from '@/components/BaseLogo'

describe('BaseLogo.vue', () => {
  const wrapper = shallowMount(BaseLogo)

  it('root element is an svg', () => {
    expect(wrapper.is('svg')).to.equal(true)
  })

  it('has default height of 35pt and default width of 50pt', () => {
    const defaultHeight = 35
    const defaultWidth = 50
    expect(wrapper.attributes().height).to.equal(`${defaultHeight}pt`)
    expect(wrapper.attributes().width).to.equal(`${defaultWidth}pt`)
  })
})
