import Logo from '@/components/Logo'
import { shallowMount } from '@vue/test-utils'
import { expect } from 'chai'

describe('Logo.vue', () => {
  const wrapper = shallowMount(Logo)
  const defaultHeight = 35
  const defaultWidth = 50
  const customSize = 70

  it('root element is an svg', () => {
    expect(wrapper.is('svg')).to.equal(true)
  })

  it('uses default height and width when no prop is passed down', () => {
    expect(wrapper.props().height).to.equal(defaultHeight)
    expect(wrapper.props().width).to.equal(defaultWidth)

    expect(wrapper.attributes().height).to.equal(`${defaultHeight}pt`)
    expect(wrapper.attributes().width).to.equal(`${defaultWidth}pt`)
  })

  it('height of svg matches height prop passed down', () => {
    wrapper.setProps({ height: customSize })
    expect(wrapper.props().height).to.equal(customSize)
    expect(wrapper.props().width).to.equal(defaultWidth)

    expect(wrapper.attributes().height).to.equal(`${customSize}pt`)
    expect(wrapper.attributes().width).to.equal(`${defaultWidth}pt`)
  })

  it('width of svg matches width prop passed down', () => {
    wrapper.setProps({ width: customSize })
    expect(wrapper.props().width).to.equal(customSize)
    expect(wrapper.props().height).to.equal(customSize)

    expect(wrapper.attributes().width).to.equal(`${customSize}pt`)
    expect(wrapper.attributes().height).to.equal(`${customSize}pt`)
  })
})
